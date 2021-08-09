from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# db = sqlite3.connect("moviedb.db")
# cursor = db.cursor()

# cursor.execute("ALTER TABLE Movies ADD year INTEGER")
# db.commit()

# new_movie = cursor.execute('INSERT INTO Movies (title, description, rating, ranking, review, img_url, year) VALUES ("Phone Book", "Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist\'s sniper rifle. Unable to leave or receive outside help, Stuart\'s negotiation with the caller leads to a jaw-dropping climax.", 7.3, 10, "My favourite character was the caller.", "https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg", 2002)')
# db.commit()

class RatingForm(FlaskForm):
    rating = StringField("Your rating out of 10, e.g. 7.5", validators=[DataRequired()])
    review = StringField("Your review of the movie.")
    submit = SubmitField("Submit")

class AddForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    year = IntegerField("Year", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    rating = IntegerField("Rating", validators=[DataRequired()])
    ranking = IntegerField("Ranking", validators=[DataRequired()])
    review = StringField("Brief Review", validators=[DataRequired()])
    image = StringField("URL Of The Cover", validators=[DataRequired()])
    submit = SubmitField("Add")



@app.route("/")
def home():
    db = sqlite3.connect("moviedb.db", timeout=2)
    cursor = db.cursor()
    table = cursor.execute("SELECT id, title, description, rating, ranking, review, img_url, year FROM Movies")
    items = table.fetchall()
    db.close()    
    return render_template("index.html", items=items)


@app.route("/edit<id>", methods=["GET", "POST"])
def edit(id):
    db = sqlite3.connect("moviedb.db")
    cursor = db.cursor()
    table = cursor.execute(f"SELECT title, rating FROM Movies WHERE id = {id}")
    items = table.fetchall()

    form = RatingForm()
    if form.validate_on_submit():

        rating = form.rating.data
        cursor.execute(f"UPDATE Movies SET rating = {rating} WHERE id = {id}")
        if form.review.data:
            review = form.review.data
            cursor.execute(f'UPDATE Movies SET review = "{review}" WHERE id = {id}')

        db.commit()
        db.close()
            
        return redirect("/")
        
    return render_template("edit.html", items = items, form=form)

@app.route("/delete<id>")
def delete(id):
    db = sqlite3.connect("moviedb.db", timeout=5)
    cursor = db.cursor()

    cursor.execute(f"DELETE FROM Movies WHERE id = {id}")
    db.commit()
    db.close()
    
    return redirect("/")

@app.route("/add", methods=["GET", "POST"])
def add():
    db = sqlite3.connect("moviedb.db")
    cursor = db.cursor()
    form = AddForm()

    if request.method == "POST":
        title = form.title.data
        description = form.description.data
        rating = form.rating.data
        ranking = form.ranking.data
        review = form.review.data
        img_url = form.image.data
        year = form.year.data 

        print(title)

        cursor.execute(f'INSERT INTO Movies (title, description, rating, ranking, review, img_url, year) VALUES ("{title}", "{description}", "{rating}", "{ranking}", "{review}", "{img_url}", "{year}")')
        db.commit()
        db.close()
        return redirect("/")

    return render_template("add.html", form = form)

if __name__ == '__main__':
    app.run(debug=True)
