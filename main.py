from flask import Flask, render_template, request, redirect, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create an application
app = Flask(__name__)

# configuring app with sql
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'  # Creating a database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating a database
db = SQLAlchemy(app)


# Creating Books class to from database
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Float(100), nullable=False)


# Creating a database file
db.create_all()

# Get all books form the database
all_books = db.session.query(Books).all()


# Adding routes

# Home
@app.route('/')
def home():
    # return statement
    return render_template('index.html', bk_list=all_books)  # Passing book database as parameter


# Delete entry from database
@app.route('/del/<int:id>')
def delete(id):  # Passing ID as parameter
    delete_book = Books.query.get(id)  # Get books in database by id
    db.session.delete(delete_book)  # Delete the entry with that id
    db.session.commit()  # Commit the changes
    return redirect(url_for('home'))


# Add book to database
@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        form = request.form.to_dict()  # Getting form details and converting it to dictionary to form key: value pairs
        new_book = Books(title=form['name'], author=form['author'], rating=float(form['rating']))  # Calling keys and
        # entering them as new entry in the database
        db.session.add(new_book)  # Adding entry in the database
        db.session.commit()  # Commit the changes
        return redirect(url_for('home'))
    return render_template('add.html')


# Add/ Change rating to/ of the book and commit to database
@app.route('/<int:id>', methods=['GET', 'POST'])
def rating(id):
    if request.method == 'POST':
        form = request.form.to_dict()  # Getting form details and converting it to dictionary to form key: value pairs
        chng_rating_book = Books.query.get(id)  # Getting books in database by id
        chng_rating_book.rating = float(form['rating'])  # Changing the rating
        db.session.commit()  # Committing the changes
        return redirect(url_for('home'))
    return render_template('rating.html', id=id, bk_list=all_books)


if __name__ == "__main__":
    app.run(debug=True)
