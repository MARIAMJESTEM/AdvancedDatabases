import json
import os
from typing import List, Any, cast
from sqlalchemy import create_engine
from database.database_queries import DatabaseQueries
from flask import Flask, render_template, request, flash, redirect, url_for
app = Flask(__name__)

app.config['SECRET_KEY'] = '27ba51b46332c22d3005b6534d881908'
LoggedIn = False
usernameDB = ""
search_term = ""


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    top10Books = query.get_top_rated_books(10)  # function return pd.DataFrame
    global LoggedIn
    if request.method == 'POST':
        if "action" in request.form and request.form["action"] == "LogOut":
            LoggedIn = False
    return render_template('home.html', LoggedIn=LoggedIn, top10Books=top10Books)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global LoggedIn
        global usernameDB
        username = request.form['username']
        password = request.form['password']
        LoggedIn = query.check_user_password(username=username, password=password)
        if LoggedIn:
            usernameDB = username
            return redirect(url_for('home'))
        else:
            flash('Given username or password is incorrect')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    global LoggedIn
    global usernameDB
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        isUserName = not query.check_is_username_taken(username=username)
        isEmail = not query.check_is_email_taken(email=email)
        if isUserName and isEmail:
            LoggedIn = True
            usernameDB = username
            query.add_new_user_to_database(username=username, password=password, email=email)
            return redirect(url_for('home'))
        elif not isUserName:
            flash('Given username is already taken')
            return redirect(url_for('signin'))
        else:
            flash('Given email is already taken')
            return redirect(url_for('signin'))
    return render_template('signin.html')


@app.route("/userbooks", methods=['GET', 'POST'])
def userbooks():
    global LoggedIn
    global usernameDB
    data = query.get_user_read_books(username=usernameDB)
    columns = ["title", "author", "genre", "release_year"]

    if request.method == 'POST':
        if "action" in request.form and request.form["action"] == "LogOut":
            LoggedIn = False
            return redirect(url_for('home'))
        title = request.form['title']

        isTitleInDB = query.check_is_title_in_user_database(username=usernameDB, book_title=title)
        if isTitleInDB:
            flash('Given book title is already added to your list!')
            return redirect(url_for('userbooks'))
        else:
            query.add_read_book_to_user_list(username=usernameDB, book_title=title)
    return render_template('userBooks.html', LoggedIn=LoggedIn, data=data, columns=columns)


@app.route("/userreviews", methods=['GET', 'POST'])
def userreview():
    global LoggedIn
    global usernameDB
    data = query.get_user_reviews(username=usernameDB)
    columns = ["title", "rating", "comment"]

    if request.method == 'POST':
        if "action" in request.form and request.form["action"] == "LogOut":
            LoggedIn = False
            return redirect(url_for('home'))
        title = request.form['title']
        review = request.form['description']
        rating = float(request.form['quantity'])

        isTitleInDB = query.check_book_exists(book_title=title)
        if isTitleInDB:
            flash('Given book title is already commented!')
            return redirect(url_for('userreview'))
        else:
            query.add_review_to_user_book(username=usernameDB, book_title=title, rating=rating, comment=review)
    return render_template('userReviews.html', LoggedIn=LoggedIn, data=data, columns=columns)


@app.route("/search", methods=['GET', 'POST'])
def search():
    global LoggedIn
    global search_term
    if request.method == 'POST':
        if "action" in request.form and request.form["action"] == "LogOut":
            LoggedIn = False
            return redirect(url_for('search'))
        search_term = request.form['search']
        try:
            bookData = query.get_search_book_by_title(book_title=search_term)
        except Exception as e:
           return render_template('search_negative.html', LoggedIn=LoggedIn, search=search_term) 
        reviews = query.get_book_reviews(book_title=search_term)
    return render_template('search.html', LoggedIn=LoggedIn, Reviews=reviews, bookData=bookData)

@app.route("/search_negative", methods=['GET', 'POST'])
def search_negative():
    global LoggedIn
    global search_term
    if request.method == 'POST':
        if "action" in request.form and request.form["action"] == "LogOut":
            LoggedIn = False
            return redirect(url_for('search_negative'))
    return render_template('search_negative.html', LoggedIn=LoggedIn, search=search_term)

if __name__ == '__main__':
    db_string = "postgresql://postgres:postgres@localhost:5432/advanced_databases"
    engine = create_engine(db_string)
    query = DatabaseQueries(engine)
    app.run(debug=True)
