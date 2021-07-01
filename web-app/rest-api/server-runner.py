from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ac381138f988698c'

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


# Init Registration Page
@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# Init Login Page
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


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
