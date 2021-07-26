from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from forms import RegistrationForm, LoginForm, BookForm, NameForm, TextAreaField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ac381138f988698c'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/stbanas/PycharmProjects/book-resource-manager/dbase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(60))
    title = db.Column(db.String(60))
    # user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, author, title):
        self.author = author
        self.title = title

    def __repr__(self):
        return f"Author('{self.author}', '{self.title}')"


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    # books = db.relationship('Book', backref='user', lazy=True)
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')" # , '{self.image_file}'

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # users = db.relatioship('User', backref='role')

    def __repr__(self):
        return f"Role( {self.name})"

# Book Schema
class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'author', 'title')

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'books')

# Role Schema
class RoleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'role')

# Init schema
book_schema = BookSchema()
books_schema = BookSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

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
@app.route('/', methods=['GET', 'POST'])
def index():
    # form = NameForm()
    # if form.validate_on_submit():
    #     # session['name'] = form.name.data
    #     user = User.query.filter_by(username=form.name.data).first()
    #     if user is None:
    #         user = User(username=form.name.data)
    #         db.session.add(user)
    #         db.session.commit()
    #         # session['known'] = False
    #     else:
    #         # session['known'] = True
    #     # session['name'] = form.name.data
    #         form.name.data = ''
    #     return redirect(url_for('index'))
    return render_template('index.html') # TODO form = formname = session.get('name'), known=session.get('known', False)

# Add Book from Capture Page
@app.route('/book/modify/add/NLP', methods=['GET', 'POST'])
def create_book_NLP():
    return render_template('speek.html', title='NLP')
# Add Book from Capture Page

@app.route('/book/modify/add/import', methods=['GET', 'POST'])
def create_book_CSV():
    return render_template('import.html', title='Import')

# Add Book from Capture Page
@app.route('/book/modify/add/capture', methods=['GET', 'POST'])
def modify_add_capture():
    return render_template('capture.html', title='Capture')

# Add Book by JSON
@app.route('/book/modify/add/json', methods=['POST','GET'])
def modify_add_json():
    author = request.json['author']
    title = request.json['title']

    new_book = Book(author, title)

    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book)


# # Create / Modify_manual endpoint
# @app.route('/book/modify/add/mode/manual', methods=['GET','POST'])
# def modify_book():
#     form = BookForm(request.form)
#     books = Book.query.all()
#     if form.validate_on_submit():
#         book = Book(author=form.author.data, title=form.title.data)
#         db.session.add(book)
#         db.session.commit()
#         flash("Added Book Successfully")
#         return redirect(url_for("create_book"))
#     return render_template("bookList.html", title="Books", form=form, books=books)

# Create / Modify_manual endpoint
@app.route('/book/modify/add/mode/manual', methods=['GET','POST'])
def create_book_manualy():
    form = BookForm(request.form)
    books = Book.query.all()
    if form.validate_on_submit():
        book = Book(author=form.author.data, title=form.title.data)
        db.session.add(book)
        db.session.commit()
        flash("Added Book Successfully")
        return redirect(url_for("create_book_manualy"))
    return render_template("addBookManualy.html", title="Add", form=form, books=books)

# Create Modify endpoint
@app.route('/book/modify/add/mode', methods=['GET','POST'])
def modify_mode():
    form = BookForm(request.form)
    books = Book.query.all()
    if form.validate_on_submit():
        book = Book(author=form.author.data, title=form.title.data)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("modify_mode"))
    return render_template("modifyMode.html", title="AddMode", form=form, books=books)
#
# # Create a Modify endpoint
# @app.route('/book/modify/add/mode', methods=['GET','POST'])
# def modify():
#         return render_template('modifyMode.html', title='AddMode')

# Create a Modify_add endpoint
@app.route('/book/modify/add', methods=['GET','POST'])
def modify_add():
    return render_template('modify.html', title='Modify')

# Get List of All Books
@app.route('/book/list', methods=['GET'])
def get_books():
    form = BookForm(request.form)
    books = Book.query.all()
    return render_template("list.html", title="List", form=form, books=books)

# Delete Book
@app.route("/book/modify/delete/<int:book_id>", methods=["GET", "POST"])
def delete_book(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return render_template("modify.html", title="Delete")

# Update Book
@app.route("/book/modify/update/<int:book_id>", methods=["GET", "POST"])
def update_book(book_id):
    book = Book.query.get(book_id)
    form = BookForm(request.form, obj=book)
    if form.validate_on_submit():
        form.populate_obj(book)
        db.session.commit()
        flash("Updated Book Successfully")
        return redirect(url_for("modify_mode")) #TODO
    # return render_template("createBooksManualy.html", title="Book", form=form, book=Book.query.all())
    return render_template("update.html", title="Update", form=form, book=book)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
