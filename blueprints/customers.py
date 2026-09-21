"""Customer record keeping."""
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import db
from models import Customer

bp = Blueprint("customers", __name__)


@bp.route("/")
def list_customers():
    q = request.args.get("q", "").strip()
    query = Customer.query
    if q:
        like = f"%{q}%"
        query = query.filter(Customer.name.ilike(like) |
                             Customer.phone.ilike(like) |
                             Customer.email.ilike(like))
    customers = query.order_by(Customer.name).all()
    return render_template("customers/list.html", customers=customers, q=q)


@bp.route("/new", methods=["GET", "POST"])
def new_customer():
    if request.method == "POST":
        c = Customer(
            name=request.form["name"].strip(),
            phone=request.form.get("phone", "").strip(),
            email=request.form.get("email", "").strip(),
            notes=request.form.get("notes", ""),
        )
        db.session.add(c)
        db.session.commit()
        flash(f"Added customer '{c.name}'.", "success")
        return redirect(url_for("customers.list_customers"))
    return render_template("customers/form.html", customer=None)


@bp.route("/<int:customer_id>")
def detail(customer_id):
    c = Customer.query.get_or_404(customer_id)
    return render_template("customers/detail.html", customer=c)
