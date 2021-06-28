from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/stbanas/PycharmProjects/book-resource-manager/books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(30))
    lastName = db.Column(db.String(20))
    title = db.Column(db.String(30))

    def __init__(self, firstName, lastName, title):
        self.firstName = firstName
        self.lastName = lastName
        self.title = title

# Book Schema
class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstName', 'lastName', 'title')

# Init schema
book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Create a Book
@app.route('/book', methods=['POST'])
def add_book():

    firstName = request.json['firstName']
    lastName = request.json['lastName']
    title = request.json['title']

    new_book = Book(firstName, lastName, title)

    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book)

#Open Main Page

@app.route('/', methods=['GET'])
def about_me():
    return render_template('home.html', title="Main Library Entrance")

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

    firstName = request.json['firstName']
    lastName = request.json['lastName']
    title = request.json['title']

    book.firstName = firstName
    book.lastName = lastName
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