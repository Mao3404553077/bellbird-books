"""Load demo data so the UI is not empty on first run.

Usage:
    flask --app app shell
    >>> from seed import load_demo_data; load_demo_data()
"""
from app import db
from models import Book, BookCopy, Customer, Order, OrderItem


def load_demo_data():
    if Book.query.first():
        print("Database already populated; skipping.")
        return

    c1 = Customer(name="Roz Ainsley", phone="07 3366 1100",
                  email="roz@bellbirdbooks.au")
    c2 = Customer(name="Jane Mitchell", phone="0412 555 014",
                  email="jane.m@example.com")
    db.session.add_all([c1, c2])

    b1 = Book(title="The Poisonwood Bible", author="Barbara Kingsolver",
              isbn="9780060788173", location_shelf="Fiction-A3",
              price_cents=2200, is_new=True, quantity=12)
    b2 = Book(title="Cloudstreet", author="Tim Winton",
              isbn="9780140276135", location_shelf="Aus-Fiction-B1",
              price_cents=1800, is_new=True, quantity=4)
    b3 = Book(title="To Kill a Mockingbird", author="Harper Lee",
              location_shelf="Classics-C2", price_cents=850,
              is_new=False)
    b4 = Book(title="The Hobbit", author="J.R.R. Tolkien",
              location_shelf="Fantasy-D1", price_cents=1200,
              is_new=False)
    db.session.add_all([b1, b2, b3, b4])
    db.session.flush()

    db.session.add_all([
        BookCopy(book_id=b3.id, condition="Very Good"),
        BookCopy(book_id=b3.id, condition="Good"),
        BookCopy(book_id=b4.id, condition="As New"),
    ])

    o1 = Order(customer_id=c2.id, status="placed",
               notes="Customer will pick up Saturday.")
    o1.items.append(OrderItem(book_id=b1.id, quantity=1,
                              unit_price_cents=b1.price_cents))
    b1.quantity -= 1
    db.session.add(o1)
    db.session.commit()
    print("Demo data loaded.")
