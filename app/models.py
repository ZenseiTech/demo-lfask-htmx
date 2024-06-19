"""Create the models for the application."""
from app import db


class Author(db.Model):
    """Create the author model."""

    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    books = db.relationship("Book", backref="author")

    def __repr__(self):
        """Return the model representation."""
        return "<Author: {}>".format(self.books)


class Book(db.Model):
    """Create the book model."""

    book_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("author.author_id"))
    title = db.Column(db.String)
