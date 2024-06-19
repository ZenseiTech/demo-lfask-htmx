from app import app, db
from flask import render_template, request, jsonify
from app.models import Author, Book

data = [{"title": "Harry", "author": "JK Rowling"}, {"title": "Lord of Rings", "author": "Whoever"}]

@app.route("/", methods=["GET"])
def home():
    books = db.session.query(Book).all()
    books_list = []

    for book in books:
        author = Author.query.get(book.author_id)
        book_object = {"id": book.book_id, "title": book.title, "author": author.name}
        books_list.append(book_object)

    return render_template("index.html", books=books_list)

@app.route("/get-book-row/<int:id>", methods=["GET"])
def get_book_row(id):
    book = Book.query.get(id)
    author = Author.query.get(book.author_id)

    return render_template("_book_row.html", book=book, author=author)


@app.route("/get-edit-form/<int:id>", methods=["GET"])
def get_edit_form(id):
    book = Book.query.get(id)
    author = Author.query.get(book.author_id)

    return render_template("_book_edit.html", book=book, author=author)


@app.route("/update/<int:id>", methods=["PUT"])
def update_book(id):
    db.session.query(Book).filter(Book.book_id == id).update({"title": request.form["title"]})
    db.session.commit()

    title = request.form["title"]
    book = Book.query.get(id)
    author = Author.query.get(book.author_id)

    return render_template("_book_update.html", book=book, author=author) 

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return ""

@app.route("/submit", methods=["POST"])
def submit():
    global_book_object = Book()

    title = request.form["title"]
    author_name = request.form["author"]

    author = db.session.query(Author).filter(Author.name == author_name).first()
    
    # check if author already exists in db
    if author:
        author_id = author.author_id
        book = Book(author_id=author_id, title=title)
        db.session.add(book)
        db.session.commit()

    else:
        author = Author(name=author_name)
        db.session.add(author)
        db.session.commit()

        book = Book(author_id=author.author_id, title=title)
        db.session.add(book)
        db.session.commit()
    
    return render_template("_book_submit.html", book=book, author=author) 
    