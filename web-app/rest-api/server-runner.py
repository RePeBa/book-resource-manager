from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import UserMixin
from flask_wtf import FlaskForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/stbanas/PycharmProjects/book-resource-manager/books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# all_books = [{'firstName': 'Philip',
#           'lastName': 'Zimbardo',
#           'title': 'Lucyfer efect'},
#
#          {'firstName': 'Herman',
#           'lastName': 'Mellvile',
#           'title': 'Mobby dick'}
#          ]

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

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, username, email, password_hash, role_id):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role_id = role_id

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'email', 'password_hash', 'role_id')

# Init user schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/', methods=['GET'])
def home():
    return render_template('auth.html', title="Home")


#Open Login Page
@app.route('/auth.login', methods=['POST', 'GET'])
def auth_login():
    return render_template('form.html')

#Open Logout Page
@app.route('/auth.logout', methods=['POST', 'GET'])
def auth_logout():
    return render_template('form.html')

#Open Register Page
@app.route('/auth.register', methods=['POST', 'GET'])
def auth_register():
    return render_template('user.html')


#Open User Page
@app.route('/user', methods=['POST', 'GET'])
def add_user():
    username = request.json["username"]
    role_id = request.json["role_id"]
    email = request.json["email"]
    password_hash = request.json["password_hash"]

    new_user = User(username, password_hash, email, role_id )

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/book', methods=['GET'])
def book():
    all_books = Book.query.all()
    print(all_books)
    return render_template('books.html', title="Books", all_books=all_books)

# Create a Book
@app.route('/book', methods=['POST','PATCH'])
def add_book():

    firstName = request.json["firstName"]
    lastName = request.json["lastName"]
    title = request.json['title']

    new_book = Book(firstName, lastName, title)

    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book)

# # Get All Books
# @app.route('/book', methods=['GET'])
# def get_books():
#     all_books = Book.query.all()
#     print(all_books)
#     result = books_schema.dump(all_books)
#     return jsonify(result)

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