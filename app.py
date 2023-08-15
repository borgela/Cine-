from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
import random
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PS-HT-Sud-Cayes-50938603038'


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/rate_movies', methods=['GET'])
def rate_movies():
    if request.method == 'POST':
        user_ratings = {}
        conn = sqlite3.connect('movies.sqlite')
        cur = conn.cursor()

        movies = cur.execute('SELECT * FROM movies').fetchall()
        for movie in movies:
            print (rating)
            if rating is not None:
                user_ratings[movie[1]] = float(rating)
                if len(user_ratings) == 2:
                    break

        if len(user_ratings) != 2:
            conn.close()
    

        session['user_ratings'] = user_ratings
        conn.close()

    conn = sqlite3.connect('movies.sqlite')
    cur = conn.cursor()
    movies = cur.execute('SELECT * FROM movies').fetchall()
    conn.close()

    random_movies = random.sample(movies, 2)
    movie1 = random_movies[0]
    movie2 = random_movies[1]
    global sample_movies
    sample_movies=[movie1,movie2]
    
    return render_template('rate_movies.html', movie1=movie1, movie2=movie2, movies=movies)

@app.route('/recommendation',methods=['GET','POST'])
def suggest_rating():
    movie1_rating=float(request.form["rating1"])
    movie2_rating=float(request.form["rating2"])
    the_rates=[]
    the_rates.append(movie1_rating)
    the_rates.append(movie2_rating)
    highest_rate=max(the_rates)
    emplacement=the_rates.index(highest_rate)
    The_highest_movie=sample_movies[emplacement]
    conn = sqlite3.connect('movies.sqlite')
    cur = conn.cursor()
    movies = cur.execute('SELECT * FROM movies').fetchall()
    suggestions=[]
    for movie in movies:
        if movie[1]==The_highest_movie[1] and movie[2]==The_highest_movie[2] and movie[3]>=The_highest_movie[3]:
            suggestions.append(movie)
        else: continue
    sug=random.choice(suggestions)
    suggestion_title=sug[0]
    suggestion_genre=sug[1]
    suggestion_director=sug[2]
    suggestion_rating=sug[3]
    return render_template('recommendation.html',suggestion_title=suggestion_title,suggestion_genre=suggestion_genre,suggestion_director=suggestion_director,suggestion_rating=suggestion_rating)






    



app.run(debug=True)
