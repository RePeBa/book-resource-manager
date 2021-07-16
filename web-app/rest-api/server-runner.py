from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from forms import RegistrationForm, LoginForm, BookForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ac381138f988698c'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/stbanas/PycharmProjects/book-resource-manager/books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50))
    title = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, author, title):
        self.author = author
        self.title = title

    def __repr__(self):
        return f"Book('{self.author}', '{self.title}')"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.authorString(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    book = db.relationship('Book', backref='user_id', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


# Book Schema
class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'author', 'title')


# Init schema
book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Init Home Page
@app.route('/', methods=[ "GET"])
def start():
    return render_template('home.html', title='Start')

# Init Capture Page
@app.route('/capture', methods=[ "GET"])
def capture():
    return render_template('capture.html', title='Capture')

# Init Registration Page
@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# Init Login Page
@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


# Create a Book
@app.route('/book', methods=['POST'])
def add_book():
    author = request.json['author']
    title = request.json['title']

    new_book = Book(author, title)

    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book)


# Get All Books
@app.route('/book', methods=['GET', 'POST'])
def get_books():
    form = BookForm()
    return render_template('books.html', title='Books', form=form)


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
