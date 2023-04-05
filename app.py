from flask import Flask, render_template, request
import pandas as pd
import requests
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'dkf3sldkjfDF23fLJ3b'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)


# classes for DB
class User(db.Model):
    __tablename__ = 'User'
    user_name = db.Column(db.String(20), primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return self.user_name + ":" + self.full_name


class Stats(db.Model):
    __tablename__ = 'Stats'
    stat_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    games_played = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Float, nullable=False)
    rebounds = db.Column(db.Float, nullable=False)
    assists = db.Column(db.Float, nullable=False)
    percent_fg = db.Column(db.Float, nullable=False)
    percent_threes = db.Column(db.Float, nullable=False)
    percent_ft = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


def add_user(user_name, full_name, email, password):
    new_user = User(user_name=user_name, full_name=full_name,
                    email=email, password=password)
    db.session.add(new_user)
    db.session.commit()


# DB routes (methods) go here
def create_stats_table():
    db.session.query(Stats).delete()
    db.session.commit()

    list1 = [2022, 2021, 2020, 2019,
             2018, 2017, 2016, 2015, 2014, 2013,
             2012, 2011, 2010, 2009, 2008, 2007,
             2006, 2005, 2004, 2003, 2002, 2001,
             2000, 1999, 1998, 1997, 1996, 1995,
             1994, 1993, 1992, 1991, 1990, 1989,
             1988, 1987, 1986, 1985, 1984, 1983,
             1982, 1981, 1980, 1979]

    list2 = ["23", "22", "21", "20",
             "19", "18", "17", "16", "15", "14",
             "13", "12", "11", "10", "09", "08",
             "07", "06", "05", "04", "03", "02",
             "01", "00", "99", "98", "97", "96",
             "95", "94", "93", "92", "91", "90",
             "89", "88", "87", "86", "85", "84",
             "83", "82", "81", "80"]

    for i in range(len(list1)):
        pd.set_option('display.max_columns', None)

        test_url = f"https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season={list1[i]}-{list2[i]}&SeasonType=Regular%20Season&StatCategory=PTS"
        r = requests.get(url=test_url).json()
        # Year, GP, PTS, REB, AST, FG_PCT, 3P%, FT%

        data_rows = r['resultSet']['rowSet']

        headers = r['resultSet']['headers']

        name_index = headers.index('PLAYER')
        gp_index = headers.index('GP')
        pts_index = headers.index('PTS')
        reb_index = headers.index('REB')
        ast_index = headers.index('AST')
        fg_index = headers.index('FG_PCT')
        three_p_index = headers.index('FG3_PCT')
        ft_p_index = headers.index('FT_PCT')

        for row in data_rows:
            new_stat = Stats(year=list1[i] + 1, name=row[name_index], games_played=row[gp_index], points=row[pts_index], rebounds=row[reb_index],
                             assists=row[ast_index], percent_fg=row[fg_index], percent_threes=row[three_p_index], percent_ft=row[ft_p_index])
            db.session.add(new_stat)
            db.session.commit()


# Web routes go here
@app.route('/')
def home():
    create_stats_table()
    return render_template("home-page.html")

# Web routes go here


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/query')
def query():
    return render_template("query.html")


@app.route('/duel')
def duel():
    return render_template("duel.html")


@app.route('/hypo-player')
def hypo_player():
    return render_template("hypo-player.html")


app.run(debug=True, host='0.0.0.0', port=81)
