from flask import Flask, request, jsonify, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from forms import BookForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/stbanas/PycharmProjects/book-resource-manager/dbase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = ['qwerty']

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50))
    title = db.Column(db.String(100))

    def __init__(self, author, title):
        self.author = author
        self.title = title

# Book Schema
class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'author', 'title')

# Init schema
book_schema = BookSchema()
books_schema = BookSchema(many=True)


# Display Add Book form
@app.route('/addbook', methods=['GET', 'POST'])
def view_book_form():
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(author=form.author.data, title=form.title.data)
        db.session.add(new_book)
        db.session.commit()
        flash('New book seved.')
    else:
        new_book = Book(author=form.author.data, title=form.title.data)
        db.session.add(new_book)
        db.session.commit()
        flash('New book seved.')
        return redirect(url_for('add_book'))
    return render_template('books.html', title='Books', form=form)

# Add Book from Body
@app.route('/book', methods=['POST'])
def add_book():
    author = request.json['author']
    title = request.json['title']

    new_book = Book(author, title)

    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book)

# Get All Books
@app.route('/book', methods=['GET'])
def get_books():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return jsonify(result)

# Get Single Book
@app.route('/book/<id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    return book_schema.jsonify(book)

# Update a Book
@app.route('/book/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)

    author = request.json['author']
    title = request.json['title']

    book.author = author
    book.title = title

    db.session.commit()

    return book_schema.jsonify(book)

# Delete Book
@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return book_schema.jsonify(book)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)