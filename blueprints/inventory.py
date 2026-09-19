"""Inventory CRUD + multi-field search."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import or_

from app import db
from models import Book, BookCopy, BOOK_CONDITIONS

bp = Blueprint("inventory", __name__)


@bp.route("/")
def list_books():
    q = request.args.get("q", "").strip()
    kind = request.args.get("kind", "")
    query = Book.query

    if q:
        like = f"%{q}%"
        query = query.filter(or_(
            Book.title.ilike(like),
            Book.author.ilike(like),
            Book.location_shelf.ilike(like),
            Book.isbn.ilike(like),
        ))
    if kind == "new":
        query = query.filter_by(is_new=True)
    elif kind == "used":
        query = query.filter_by(is_new=False)

    books = query.order_by(Book.title).all()
    return render_template("inventory/list.html", books=books, q=q,
                           kind=kind)


@bp.route("/new", methods=["GET", "POST"])
def new_book():
    if request.method == "POST":
        is_new = request.form.get("is_new") == "on"
        book = Book(
            title=request.form["title"].strip(),
            author=request.form["author"].strip(),
            isbn=request.form.get("isbn", "").strip() or None,
            location_shelf=request.form["location_shelf"].strip(),
            price_cents=int(float(request.form["price"]) * 100),
            is_new=is_new,
            quantity=int(request.form.get("quantity", 0) or 0) if is_new else 0,
            notes=request.form.get("notes", ""),
        )
        db.session.add(book)
        db.session.flush()

        # For second-hand titles, accept one initial copy on creation.
        if not is_new:
            copy = BookCopy(
                book_id=book.id,
                condition=request.form.get("condition", "Good"),
            )
            db.session.add(copy)

        db.session.commit()
        flash(f"Added '{book.title}'.", "success")
        return redirect(url_for("inventory.detail", book_id=book.id))

    return render_template("inventory/form.html", book=None,
                           conditions=BOOK_CONDITIONS)


@bp.route("/<int:book_id>")
def detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("inventory/detail.html", book=book)


@bp.route("/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == "POST":
        book.title = request.form["title"].strip()
        book.author = request.form["author"].strip()
        book.isbn = request.form.get("isbn", "").strip() or None
        book.location_shelf = request.form["location_shelf"].strip()
        book.price_cents = int(float(request.form["price"]) * 100)
        if book.is_new:
            book.quantity = int(request.form.get("quantity", 0) or 0)
        book.notes = request.form.get("notes", "")
        db.session.commit()
        flash("Book updated.", "success")
        return redirect(url_for("inventory.detail", book_id=book.id))

    return render_template("inventory/form.html", book=book,
                           conditions=BOOK_CONDITIONS)


@bp.route("/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash(f"Deleted '{book.title}'.", "success")
    return redirect(url_for("inventory.list_books"))
