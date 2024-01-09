from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


db = SQLAlchemy()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book_shelf.db"
db.init_app(app=app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()

all_books = []
with app.app_context():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books_from_db = result.scalars()
    for obj in all_books_from_db:
        all_books.append(obj)
print(all_books)


@app.route("/")
def home():
    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        with app.app_context():
            new_book = Book(
                title=request.form["book_name"],
                author=request.form["book_author"],
                rating=request.form["book_rating"],
            )
            db.session.add(new_book)
            db.session.commit()
        with app.app_context():
            book = db.session.execute(
                db.select(Book).where(Book.title == request.form["book_name"])
            ).scalar()
            if book:
                all_books.append(book)

        return redirect("/")
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True, port=4000)
