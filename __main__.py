import json
import os
from typing import List, Any, cast
from sqlalchemy import create_engine
from database_queries import DatabaseQueries
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = '27ba51b46332c22d3005b6534d881908'
LoggedIn = False


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    #TODO get list of 10 best rated books
    top10Books = [['Genre1','title1', 'moredata1'],['genre2', 'title2', 'moredata2'],['genre3', 'title3', 'moredata3']]
    global LoggedIn
    if request.method == 'POST':
        if "action" in request.form and request.form["action"] == "LogOut":
            LoggedIn = False
    return render_template('home.html',LoggedIn = LoggedIn, top10Books = top10Books)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global LoggedIn
        username = request.form['username']
        password = request.form['password']
        LoggedIn = query.check_user_password(username=username, password=password)
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
        isUserName = True  # Here assign the response from data base
        isEmail = True  # Here assign the response from data base
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
        {"Title": "Lalka", "Author": "Bolesław Prus", "Genre": "powieść", "Date": "25.04.2023r."},
        {"Title": "Lalka", "Author": "Bolesław Prus", "Genre": "powieść", "Date": "25.04.2023r."},
        {"Title": "Lalka", "Author": "Bolesław Prus", "Genre": "powieść", "Date": "25.04.2023r."},
        {"Title": "Lalka", "Author": "Bolesław Prus", "Genre": "powieść", "Date": "25.04.2023r."},
        {"Title": "Lalka", "Author": "Bolesław Prus", "Genre": "powieść", "Date": "25.04.2023r."},
        {"Title": "Lalka", "Author": "Bolesław Prus", "Genre": "powieść", "Date": "25.04.2023r."},
        {"Title": "Lalka", "Author": "Bolesław Prus", "Genre": "powieść", "Date": "25.04.2023r."},
        {"Title": "Lalka", "Author": "Bolesław Prus", "Genre": "powieść", "Date": "25.04.2023r."}
    ]
    columns = ["Title", "Author", "Genre", "Date"]
    if request.method == 'POST':
        if "action" in request.form and request.form["action"] == "LogOut":
            LoggedIn = False
            return redirect(url_for('home'))
        title = request.form['title']
        rating = request.form['quantity']
        # TODO check if given title is already in user database
        isTitleInDB = True  # Here assign the response from data base
        if isTitleInDB:
            flash('Given book title is already added to your list!')
            return redirect(url_for('userbooks'))
    return render_template('userBooks.html', LoggedIn=LoggedIn, data=data, columns=columns)


@app.route("/userreviews", methods=['GET', 'POST'])
def userreview():
    global LoggedIn
    # TODO
    data = [
        {"Title": "Lalka",
         "Review": "Top książka no złoto po prostu, chce sprawdzić jak dużo tekstu się zachowa w tablei dlatego jescze może coś popisze a w sumie to mogłabym skopiować coś ale jest tak późno że nie myśle o tym już a przynajmniej sbie coś popisze bo pisanie kodu to z pisaniem się rozmywa tu jest pisanie ale do przeglądarki bo cały czas coś nie działa"},
        {"Title": "Lalka",
         "Review": "Top książka no złoto po prostu, chce sprawdzić jak dużo tekstu się zachowa w tablei dlatego jescze może coś popisze a w sumie to mogłabym skopiować coś ale jest tak późno że nie myśle o tym już a przynajmniej sbie coś popisze bo pisanie kodu to z pisaniem się rozmywa tu jest pisanie ale do przeglądarki bo cały czas coś nie działa"},
        {"Title": "Lalka",
         "Review": "Top książka no złoto po prostu, chce sprawdzić jak dużo tekstu się zachowa w tablei dlatego jescze może coś popisze a w sumie to mogłabym skopiować coś ale jest tak późno że nie myśle o tym już a przynajmniej sbie coś popisze bo pisanie kodu to z pisaniem się rozmywa tu jest pisanie ale do przeglądarki bo cały czas coś nie działa"},
        {"Title": "Lalka",
         "Review": "Top książka no złoto po prostu, chce sprawdzić jak dużo tekstu się zachowa w tablei dlatego jescze może coś popisze a w sumie to mogłabym skopiować coś ale jest tak późno że nie myśle o tym już a przynajmniej sbie coś popisze bo pisanie kodu to z pisaniem się rozmywa tu jest pisanie ale do przeglądarki bo cały czas coś nie działa"},
        {"Title": "Lalka",
         "Review": "Top książka no złoto po prostu, chce sprawdzić jak dużo tekstu się zachowa w tablei dlatego jescze może coś popisze a w sumie to mogłabym skopiować coś ale jest tak późno że nie myśle o tym już a przynajmniej sbie coś popisze bo pisanie kodu to z pisaniem się rozmywa tu jest pisanie ale do przeglądarki bo cały czas coś nie działa"},
        {"Title": "Lalka",
         "Review": "Top książka no złoto po prostu, chce sprawdzić jak dużo tekstu się zachowa w tablei dlatego jescze może coś popisze a w sumie to mogłabym skopiować coś ale jest tak późno że nie myśle o tym już a przynajmniej sbie coś popisze bo pisanie kodu to z pisaniem się rozmywa tu jest pisanie ale do przeglądarki bo cały czas coś nie działa"}
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
        isTitleInDB = False  # Here assign the response from data base
        if isTitleInDB:
            flash('Given book title is already commented!')
            return redirect(url_for('userreview'))
    return render_template('userReviews.html', LoggedIn=LoggedIn, data=data, columns=columns)


@app.route("/search", methods=['GET','POST'])
def search():
    global LoggedIn
    if request.method == 'POST':
        if "action" in request.form and request.form["action"] == "LogOut":
            print("hi")
            LoggedIn = False
            return redirect(url_for('search'))
        search_term = request.form['search']
        #TODO get book data 
        bookData =['Lalka', 'Bolesław Prus', 'The Doll (Polish: Lalka) is the second of four acclaimed novels by the Polish writer Bolesław Prus (real name Aleksander Głowacki). It was composed for periodical serialization in 1887–1889 and appeared in book form in 1890.The Doll has been regarded by some, including Nobel laureate Czesław Miłosz, as the greatest Polish novel.[1] According to Prus biographer Zygmunt Szweykowski, it may be unique in 19th-century world literature as a comprehensive, compelling picture of an entire society.', 'genre']
        #TODO get book reviews 
        reviews = [
        {'text': 'An extremely powerful story of a young Southern Negro, from his late high school days through three years of college to his life in Harlem.His early training prepared him for a life of humility before white men, but through injustices- large and small, he came to realize that he was an invisible man. People saw in him only a reflection of their preconceived ideas of what he was, denied his individuality, and ultimately did not see him at all. This theme, which has implications far beyond the obvious racial parallel, is skillfully handled. The incidents of the story are wholly absorbing. The boy\'s dismissal from college because of an innocent mistake, his shocked reaction to the anonymity of the North and to Harlem, his nightmare experiences on a one-day job in a paint factory and in the hospital, his lightning success as the Harlem leader of a communistic organization known as the Brotherhood, his involvement in black versus white and black versus black clashes and his disillusion and understanding of his invisibility- all climax naturally in scenes of violence and riot, followed by a retreat which is both literal and figurative. Parts of this experience may have been told before, but never with such freshness, intensity and power.This is Ellison\'s first novel, but he has complete control of his story and his style. Watch it.', 'rating': '1'},
        {'text': 'An extremely powerful story of a young Southern Negro, from his late high school days through three years of college to his life in Harlem.His early training prepared him for a life of humility before white men, but through injustices- large and small, he came to realize that he was an invisible man. People saw in him only a reflection of their preconceived ideas of what he was, denied his individuality, and ultimately did not see him at all. This theme, which has implications far beyond the obvious racial parallel, is skillfully handled. The incidents of the story are wholly absorbing. The boy\'s dismissal from college because of an innocent mistake, his shocked reaction to the anonymity of the North and to Harlem, his nightmare experiences on a one-day job in a paint factory and in the hospital, his lightning success as the Harlem leader of a communistic organization known as the Brotherhood, his involvement in black versus white and black versus black clashes and his disillusion and understanding of his invisibility- all climax naturally in scenes of violence and riot, followed by a retreat which is both literal and figurative. Parts of this experience may have been told before, but never with such freshness, intensity and power.This is Ellison\'s first novel, but he has complete control of his story and his style. Watch it.', 'rating': '1'},
        {'text': 'An extremely powerful story of a young Southern Negro, from his late high school days through three years of college to his life in Harlem.His early training prepared him for a life of humility before white men, but through injustices- large and small, he came to realize that he was an invisible man. People saw in him only a reflection of their preconceived ideas of what he was, denied his individuality, and ultimately did not see him at all. This theme, which has implications far beyond the obvious racial parallel, is skillfully handled. The incidents of the story are wholly absorbing. The boy\'s dismissal from college because of an innocent mistake, his shocked reaction to the anonymity of the North and to Harlem, his nightmare experiences on a one-day job in a paint factory and in the hospital, his lightning success as the Harlem leader of a communistic organization known as the Brotherhood, his involvement in black versus white and black versus black clashes and his disillusion and understanding of his invisibility- all climax naturally in scenes of violence and riot, followed by a retreat which is both literal and figurative. Parts of this experience may have been told before, but never with such freshness, intensity and power.This is Ellison\'s first novel, but he has complete control of his story and his style. Watch it.', 'rating': '1'},
        {'text': 'An extremely powerful story of a young Southern Negro, from his late high school days through three years of college to his life in Harlem.His early training prepared him for a life of humility before white men, but through injustices- large and small, he came to realize that he was an invisible man. People saw in him only a reflection of their preconceived ideas of what he was, denied his individuality, and ultimately did not see him at all. This theme, which has implications far beyond the obvious racial parallel, is skillfully handled. The incidents of the story are wholly absorbing. The boy\'s dismissal from college because of an innocent mistake, his shocked reaction to the anonymity of the North and to Harlem, his nightmare experiences on a one-day job in a paint factory and in the hospital, his lightning success as the Harlem leader of a communistic organization known as the Brotherhood, his involvement in black versus white and black versus black clashes and his disillusion and understanding of his invisibility- all climax naturally in scenes of violence and riot, followed by a retreat which is both literal and figurative. Parts of this experience may have been told before, but never with such freshness, intensity and power.This is Ellison\'s first novel, but he has complete control of his story and his style. Watch it.', 'rating': '1'},
        {'text': 'An extremely powerful story of a young Southern Negro, from his late high school days through three years of college to his life in Harlem.His early training prepared him for a life of humility before white men, but through injustices- large and small, he came to realize that he was an invisible man. People saw in him only a reflection of their preconceived ideas of what he was, denied his individuality, and ultimately did not see him at all. This theme, which has implications far beyond the obvious racial parallel, is skillfully handled. The incidents of the story are wholly absorbing. The boy\'s dismissal from college because of an innocent mistake, his shocked reaction to the anonymity of the North and to Harlem, his nightmare experiences on a one-day job in a paint factory and in the hospital, his lightning success as the Harlem leader of a communistic organization known as the Brotherhood, his involvement in black versus white and black versus black clashes and his disillusion and understanding of his invisibility- all climax naturally in scenes of violence and riot, followed by a retreat which is both literal and figurative. Parts of this experience may have been told before, but never with such freshness, intensity and power.This is Ellison\'s first novel, but he has complete control of his story and his style. Watch it.', 'rating': '1'},
        {'text': 'An extremely powerful story of a young Southern Negro, from his late high school days through three years of college to his life in Harlem.His early training prepared him for a life of humility before white men, but through injustices- large and small, he came to realize that he was an invisible man. People saw in him only a reflection of their preconceived ideas of what he was, denied his individuality, and ultimately did not see him at all. This theme, which has implications far beyond the obvious racial parallel, is skillfully handled. The incidents of the story are wholly absorbing. The boy\'s dismissal from college because of an innocent mistake, his shocked reaction to the anonymity of the North and to Harlem, his nightmare experiences on a one-day job in a paint factory and in the hospital, his lightning success as the Harlem leader of a communistic organization known as the Brotherhood, his involvement in black versus white and black versus black clashes and his disillusion and understanding of his invisibility- all climax naturally in scenes of violence and riot, followed by a retreat which is both literal and figurative. Parts of this experience may have been told before, but never with such freshness, intensity and power.This is Ellison\'s first novel, but he has complete control of his story and his style. Watch it.', 'rating': '1'},
        {'text': 'An extremely powerful story of a young Southern Negro, from his late high school days through three years of college to his life in Harlem.His early training prepared him for a life of humility before white men, but through injustices- large and small, he came to realize that he was an invisible man. People saw in him only a reflection of their preconceived ideas of what he was, denied his individuality, and ultimately did not see him at all. This theme, which has implications far beyond the obvious racial parallel, is skillfully handled. The incidents of the story are wholly absorbing. The boy\'s dismissal from college because of an innocent mistake, his shocked reaction to the anonymity of the North and to Harlem, his nightmare experiences on a one-day job in a paint factory and in the hospital, his lightning success as the Harlem leader of a communistic organization known as the Brotherhood, his involvement in black versus white and black versus black clashes and his disillusion and understanding of his invisibility- all climax naturally in scenes of violence and riot, followed by a retreat which is both literal and figurative. Parts of this experience may have been told before, but never with such freshness, intensity and power.This is Ellison\'s first novel, but he has complete control of his story and his style. Watch it.', 'rating': '1'},
        {'text': 'An extremely powerful story of a young Southern Negro, from his late high school days through three years of college to his life in Harlem.His early training prepared him for a life of humility before white men, but through injustices- large and small, he came to realize that he was an invisible man. People saw in him only a reflection of their preconceived ideas of what he was, denied his individuality, and ultimately did not see him at all. This theme, which has implications far beyond the obvious racial parallel, is skillfully handled. The incidents of the story are wholly absorbing. The boy\'s dismissal from college because of an innocent mistake, his shocked reaction to the anonymity of the North and to Harlem, his nightmare experiences on a one-day job in a paint factory and in the hospital, his lightning success as the Harlem leader of a communistic organization known as the Brotherhood, his involvement in black versus white and black versus black clashes and his disillusion and understanding of his invisibility- all climax naturally in scenes of violence and riot, followed by a retreat which is both literal and figurative. Parts of this experience may have been told before, but never with such freshness, intensity and power.This is Ellison\'s first novel, but he has complete control of his story and his style. Watch it.', 'rating': '1'}

    ]
    return render_template('search.html',LoggedIn = LoggedIn, Reviews=reviews, bookData= bookData)

if __name__ == '__main__':
    db_string = "postgresql://postgres:postgres@localhost:5432/advanced_databases"
    engine = create_engine(db_string)
    query = DatabaseQueries(engine)
    app.run(debug=True)
