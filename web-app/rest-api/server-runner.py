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
    author = db.Column(db.String(40))
    title = db.Column(db.String(40))

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
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# Home Page

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='Home Page')


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
