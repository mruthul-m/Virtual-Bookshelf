from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


app = Flask(__name__)

all_books = []


@app.route("/")
def home():
    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        data = {
            "title": request.form["book_name"],
            "author": request.form["book_author"],
            "rating": request.form["book_rating"],
        }
        all_books.append(data)
        print(all_books)
        return redirect("/")
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True, port=4000)
