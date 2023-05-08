import json
import os
from typing import List, Any, cast

from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = '27ba51b46332c22d3005b6534d881908'
LoggedIn = False

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    global LoggedIn
    if request.method == 'POST':
        if "action" in request.form and request.form["action"] == "LogOut":
            LoggedIn = False
    return render_template('home.html',LoggedIn = LoggedIn)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global LoggedIn
        username = request.form['username']
        password = request.form['password']
        # TODO check if given user data is correct
        LoggedIn = True # Here assign the response from data base
        if LoggedIn:
            return redirect(url_for('home'))
        else:
            flash('Given username or password is incorrect')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    global LoggedIn
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # TODO check if given email and username are already in database
        isUserName = True # Here assign the response from data base
        isEmail = True # Here assign the response from data base
        if isUserName and isEmail:
            LoggedIn = True
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
    # TODO
    data = [
        {"Title": "Lalka", "Author": "Bolesław Prus", "Genre": "powieść", "Date":"25.04.2023r."},
        {"Title": "Lalka", "Author": "Bolesław Prus", "Genre": "powieść", "Date":"25.04.2023r."},
        {"Title": "Lalka", "Author": "Bolesław Prus", "Genre": "powieść", "Date":"25.04.2023r."},
        {"Title": "Lalka", "Author": "Bolesław Prus", "Genre": "powieść", "Date":"25.04.2023r."},
        {"Title": "Lalka", "Author": "Bolesław Prus", "Genre": "powieść", "Date":"25.04.2023r."},
        {"Title": "Lalka", "Author": "Bolesław Prus", "Genre": "powieść", "Date":"25.04.2023r."},
        {"Title": "Lalka", "Author": "Bolesław Prus", "Genre": "powieść", "Date":"25.04.2023r."},
        {"Title": "Lalka", "Author": "Bolesław Prus", "Genre": "powieść", "Date":"25.04.2023r."}
    ]
    columns = ["Title", "Author", "Genre","Date"]
    if request.method == 'POST':
        if "action" in request.form and request.form["action"] == "LogOut":
            LoggedIn = False
            return redirect(url_for('home'))
        title = request.form['title']
        rating = request.form['quantity']
        # TODO check if given title is already in user database
        isTitleInDB = True # Here assign the response from data base
        if isTitleInDB:
            flash('Given book title is already added to your list!')
            return redirect(url_for('userbooks'))
    return render_template('userBooks.html',LoggedIn= LoggedIn, data=data, columns=columns)

@app.route("/userreviews", methods=['GET', 'POST'])
def userreview():
    global LoggedIn
    # TODO
    data = [
        {"Title": "Lalka", "Review": "Top książka no złoto po prostu, chce sprawdzić jak dużo tekstu się zachowa w tablei dlatego jescze może coś popisze a w sumie to mogłabym skopiować coś ale jest tak późno że nie myśle o tym już a przynajmniej sbie coś popisze bo pisanie kodu to z pisaniem się rozmywa tu jest pisanie ale do przeglądarki bo cały czas coś nie działa"},
        {"Title": "Lalka", "Review": "Top książka no złoto po prostu, chce sprawdzić jak dużo tekstu się zachowa w tablei dlatego jescze może coś popisze a w sumie to mogłabym skopiować coś ale jest tak późno że nie myśle o tym już a przynajmniej sbie coś popisze bo pisanie kodu to z pisaniem się rozmywa tu jest pisanie ale do przeglądarki bo cały czas coś nie działa"},
        {"Title": "Lalka", "Review": "Top książka no złoto po prostu, chce sprawdzić jak dużo tekstu się zachowa w tablei dlatego jescze może coś popisze a w sumie to mogłabym skopiować coś ale jest tak późno że nie myśle o tym już a przynajmniej sbie coś popisze bo pisanie kodu to z pisaniem się rozmywa tu jest pisanie ale do przeglądarki bo cały czas coś nie działa"},
        {"Title": "Lalka", "Review": "Top książka no złoto po prostu, chce sprawdzić jak dużo tekstu się zachowa w tablei dlatego jescze może coś popisze a w sumie to mogłabym skopiować coś ale jest tak późno że nie myśle o tym już a przynajmniej sbie coś popisze bo pisanie kodu to z pisaniem się rozmywa tu jest pisanie ale do przeglądarki bo cały czas coś nie działa"},
        {"Title": "Lalka", "Review": "Top książka no złoto po prostu, chce sprawdzić jak dużo tekstu się zachowa w tablei dlatego jescze może coś popisze a w sumie to mogłabym skopiować coś ale jest tak późno że nie myśle o tym już a przynajmniej sbie coś popisze bo pisanie kodu to z pisaniem się rozmywa tu jest pisanie ale do przeglądarki bo cały czas coś nie działa"},
        {"Title": "Lalka", "Review": "Top książka no złoto po prostu, chce sprawdzić jak dużo tekstu się zachowa w tablei dlatego jescze może coś popisze a w sumie to mogłabym skopiować coś ale jest tak późno że nie myśle o tym już a przynajmniej sbie coś popisze bo pisanie kodu to z pisaniem się rozmywa tu jest pisanie ale do przeglądarki bo cały czas coś nie działa"}
]
    columns = ["Title", "Review"]
    
    if request.method == 'POST':
        if "action" in request.form and request.form["action"] == "LogOut":
            LoggedIn = False
            return redirect(url_for('home'))
        title = request.form['title']
        review = request.form['description']
        # TODO check if given title is already in user database
        # TODO add review to database
        isTitleInDB = False # Here assign the response from data base
        if isTitleInDB:
            flash('Given book title is already commented!')
            return redirect(url_for('userreview'))
    return render_template('userReviews.html',LoggedIn = LoggedIn, data=data, columns=columns)


@app.route("/search", methods=['POST'])
def search():
    global LoggedIn
    if request.method == 'POST':
        if "action" in request.form and request.form["action"] == "LogOut":
            LoggedIn = False
            return redirect(url_for('search'))
        search_term = request.form['search']

    return render_template('search.html',LoggedIn = LoggedIn)

if __name__ == '__main__':
    app.run(debug=True)
