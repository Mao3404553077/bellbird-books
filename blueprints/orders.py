"""Order creation and status tracking."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from app import db
from models import (Order, OrderItem, Customer, Book, BookCopy,
                    ORDER_STATUSES)

bp = Blueprint("orders", __name__)


@bp.route("/")
def list_orders():
    status = request.args.get("status", "").strip()
    query = Order.query
    if status in ORDER_STATUSES:
        query = query.filter_by(status=status)
    orders = query.order_by(Order.order_date.desc()).all()
    return render_template("orders/list.html", orders=orders,
                           status=status, statuses=ORDER_STATUSES)


@bp.route("/new", methods=["GET", "POST"])
def new_order():
    customers = Customer.query.order_by(Customer.name).all()
    books = Book.query.order_by(Book.title).all()
    if request.method == "POST":
        customer_id = int(request.form["customer_id"])
        order = Order(
            customer_id=customer_id,
            status="placed",
            notes=request.form.get("notes", ""),
        )
        # One line item per submitted row.
        book_ids = request.form.getlist("book_id")
        for bid in book_ids:
            if not bid:
                continue
            book = Book.query.get(int(bid))
            if not book:
                continue
            qty = int(request.form.get(f"qty_{bid}", 1) or 1)
            item = OrderItem(
                book_id=book.id,
                quantity=qty if book.is_new else 1,
                unit_price_cents=book.price_cents,
            )
            if book.is_new:
                book.quantity = max(0, book.quantity - qty)
            else:
                # Attach the first unsold used copy.
                copy = book.copies.filter_by(is_sold=False).first()
                if copy:
                    copy.is_sold = True
                    item.book_copy_id = copy.id
            order.items.append(item)
        db.session.add(order)
        db.session.commit()
        flash(f"Order #{order.id} created.", "success")
        return redirect(url_for("orders.detail", order_id=order.id))

    return render_template("orders/form.html", customers=customers,
                           books=books)


@bp.route("/<int:order_id>")
def detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("orders/detail.html", order=order,
                           statuses=ORDER_STATUSES)


@bp.route("/<int:order_id>/status", methods=["POST"])
def update_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get("status")
    if new_status not in ORDER_STATUSES:
        abort(400)
    order.status = new_status
    db.session.commit()
    flash(f"Order #{order.id} marked as {new_status}.", "success")
    return redirect(url_for("orders.detail", order_id=order.id))
