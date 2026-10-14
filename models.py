"""SQLAlchemy models for Bellbird Books.

Core domain rules (drawn from the Project Charter):

* New books are tracked by *quantity* per title (4,200 titles at the front).
* Second-hand books are recorded *per physical copy* (2,500 copies in the
  back room), each with its own condition grade.
* Orders move through four states: placed -> arrived -> collected, with
  cancelled as an exit.
"""
from datetime import datetime, date
from extensions import db


# --- Look-up tables -----------------------------------------------------

ORDER_STATUSES = ("placed", "arrived", "collected", "cancelled")
BOOK_CONDITIONS = ("As New", "Very Good", "Good", "Fair", "Poor")


# --- Models -------------------------------------------------------------

class Book(db.Model):
    """A title. For new books ``quantity`` tracks how many copies are on
    the shelf. For second-hand titles each physical copy lives in
    :class:`BookCopy` and ``quantity`` is ignored."""

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    author = db.Column(db.String(255), nullable=False, index=True)
    isbn = db.Column(db.String(20), index=True)
    location_shelf = db.Column(db.String(64), nullable=False,
                               comment="e.g. Fiction-A3, Back-Room-B")
    price_cents = db.Column(db.Integer, nullable=False, default=0)
    is_new = db.Column(db.Boolean, default=True, nullable=False)
    quantity = db.Column(db.Integer, default=0,
                        comment="Used only when is_new is True")
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    copies = db.relationship("BookCopy", backref="book", lazy="dynamic",
                             cascade="all, delete-orphan")

    @property
    def used_stock(self):
        """Number of unsold second-hand copies on hand."""
        if self.is_new:
            return self.quantity
        return self.copies.filter_by(is_sold=False).count()

    def __repr__(self):
        return f"<Book {self.id} {self.title!r}>"


class BookCopy(db.Model):
    """One physical second-hand copy."""
    __tablename__ = "book_copies"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    condition = db.Column(db.String(20), nullable=False, default="Good")
    is_sold = db.Column(db.Boolean, default=False, index=True)
    acquired_date = db.Column(db.Date, default=date.today)
    notes = db.Column(db.Text)


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(32))
    email = db.Column(db.String(120))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship("Order", backref="customer", lazy="dynamic")

    def __repr__(self):
        return f"<Customer {self.id} {self.name!r}>"


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"),
                            nullable=False)
    status = db.Column(db.String(20), default="placed", nullable=False,
                       index=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    items = db.relationship("OrderItem", backref="order",
                            cascade="all, delete-orphan")

    @property
    def total_cents(self):
        return sum((i.unit_price_cents or 0) * (i.quantity or 1)
                   for i in self.items)

    @property
    def total_display(self):
        return f"${self.total_cents / 100:,.2f}"


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"),
                        nullable=False)
    # Either a new-book line (book_id + quantity) OR a single second-hand
    # copy (book_copy_id), never both.
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    book_copy_id = db.Column(db.Integer, db.ForeignKey("book_copies.id"))
    quantity = db.Column(db.Integer, default=1)
    unit_price_cents = db.Column(db.Integer, default=0)

    book = db.relationship("Book")
    book_copy = db.relationship("BookCopy")
