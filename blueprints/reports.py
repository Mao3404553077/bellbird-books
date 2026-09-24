"""Counter-facing reports: live stock levels and pending order queue."""
from flask import Blueprint, render_template

from app import db
from models import Book, Order, BookCopy

bp = Blueprint("reports", __name__)


@bp.route("/")
def dashboard():
    total_titles = Book.query.count()
    new_titles = Book.query.filter_by(is_new=True).count()
    used_titles = Book.query.filter_by(is_new=False).count()
    used_copies_unsold = BookCopy.query.filter_by(is_sold=False).count()
    pending_orders = (Order.query.filter(Order.status.in_(
        ["placed", "arrived"])).order_by(Order.order_date.desc()).all())
    low_stock = (Book.query.filter(Book.is_new == True,
                                   Book.quantity <= 3)
                 .order_by(Book.quantity).all())
    return render_template("reports/dashboard.html",
                           total_titles=total_titles,
                           new_titles=new_titles,
                           used_titles=used_titles,
                           used_copies_unsold=used_copies_unsold,
                           pending_orders=pending_orders,
                           low_stock=low_stock)
