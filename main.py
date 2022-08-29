from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

db = SQLAlchemy(app)


##CREATE A FORM
class CreateEntry(FlaskForm):
    name = StringField(label='Book Name', validators=[DataRequired()])
    author = StringField(label='Book Author', validators=[DataRequired()])
    rating = StringField(label='Rating', validators=[DataRequired()])
    submit = SubmitField(label='Add Book')


##CREATE TABLE
class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()


@app.route('/')
def home():
    ##READ ALL RECORDS
    all_books = Library.query.all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    form = CreateEntry()
    if form.validate_on_submit():
        # CREATE RECORD
        new_book = Library(name=form.name.data, author=form.author.data, rating=form.rating.data)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('add.html', form=form)


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    if request.method == 'GET':
        book_id = request.args.get('id', type=int)
        book_to_edit = Library.query.get(book_id)
        return render_template('edit.html', book_selected=book_to_edit)
    else:
        # UPDATE RECORD
        changed_rating = request.form['new_rating']
        book_to_edit_id = request.form['id']
        book_to_edit = Library.query.get(book_to_edit_id)
        book_to_edit.rating = changed_rating
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/delete')
def delete():
    book_id = request.args.get('id', type=int)
    # DELETE A RECORD BY ID
    book_to_delete = Library.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
