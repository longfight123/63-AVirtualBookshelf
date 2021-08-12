"""A Virtual Bookshelf

This 'Flask' app creates a virtual bookshelf that the user can
add books and ratings to. Data is stored inside an SQLite database.

This script requires that 'Flask', 'Flask-SQLAlchemy' be installed within the Python
environment you are running this script in.

"""

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
all_books = []


class Books(db.Model):
    """
    A class used to represent a Books table in a database.

    ...

    Attributes
    ----------
    id: db.Column
        an integer column representing the primary key
    title: db.Column
        a string column representing the title of the book
    author: db.Column
        a string column representing the author of the book
    rating: db.Column
        a float column representing the rating of the book
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


try:
    db.create_all()
except:
    pass


@app.route('/')
def home():
    """the landing page, displays all books in the database
    """
    all_books = Books.query.all()
    return render_template('index.html', all_books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    """displays the form to add new books to the database

    GET: displays form to add new books
    POST: add a book to the database, redirect to landing page
    """
    if request.method == 'POST':
        # book_dictionary = {
        #     'title': request.form['book_name'],
        #     'author': request.form['book_author'],
        #     'rating': request.form['book_rating']
        # }
        # all_books.append(book_dictionary)
        # print(all_books)
        book = Books(title=request.form['book_name'], author=request.form['book_author'], rating=request.form['book_rating'])
        db.session.add(book)
        db.session.commit()
        print(Books.query.all())
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    """allows you to edit the id_number in the database

    GET: displays the form to edit the id number of a book
    POST: updates the id number in the database, redirects to landing page
    """
    id_number = request.args.get('id_number')
    if request.method == 'POST':
        book = Books.query.filter_by(id=id_number).first()
        book.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))
    book = Books.query.filter_by(id=id_number).first()
    return render_template('edit.html', book=book)


@app.route('/delete')
def delete():
    """deletes a book in the database

    GET: delete a book in the database
    """
    id_number = int(request.args.get('id_number'))
    book = Books.query.get(id_number)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

