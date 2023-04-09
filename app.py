from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import pandas as pd
import requests
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dkf3sldkjfDF23fLJ3b'
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
# def create_stats_table():
#     db.session.query(Stats).delete()
#     db.session.commit()

#     list1 = [2022, 2021, 2020, 2019,
#              2018, 2017, 2016, 2015, 2014, 2013,
#              2012, 2011, 2010, 2009, 2008, 2007,
#              2006, 2005, 2004, 2003, 2002, 2001,
#              2000, 1999, 1998, 1997, 1996, 1995,
#              1994, 1993, 1992, 1991, 1990, 1989,
#              1988, 1987, 1986, 1985, 1984, 1983,
#              1982, 1981, 1980, 1979]

#     list2 = ["23", "22", "21", "20",
#              "19", "18", "17", "16", "15", "14",
#              "13", "12", "11", "10", "09", "08",
#              "07", "06", "05", "04", "03", "02",
#              "01", "00", "99", "98", "97", "96",
#              "95", "94", "93", "92", "91", "90",
#              "89", "88", "87", "86", "85", "84",
#              "83", "82", "81", "80"]

#     for i in range(len(list1)):
#         pd.set_option('display.max_columns', None)

#         test_url = f"https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season={list1[i]}-{list2[i]}&SeasonType=Regular%20Season&StatCategory=PTS"
#         r = requests.get(url=test_url).json()
#         # Year, GP, PTS, REB, AST, FG_PCT, 3P%, FT%

#         data_rows = r['resultSet']['rowSet']

#         headers = r['resultSet']['headers']

#         name_index = headers.index('PLAYER')
#         gp_index = headers.index('GP')
#         pts_index = headers.index('PTS')
#         reb_index = headers.index('REB')
#         ast_index = headers.index('AST')
#         fg_index = headers.index('FG_PCT')
#         three_p_index = headers.index('FG3_PCT')
#         ft_p_index = headers.index('FT_PCT')

#         for row in data_rows:
#             new_stat = Stats(year=list1[i] + 1, name=row[name_index], games_played=row[gp_index], points=row[pts_index], rebounds=row[reb_index],
#                              assists=row[ast_index], percent_fg=row[fg_index], percent_threes=row[three_p_index], percent_ft=row[ft_p_index])
#             db.session.add(new_stat)
#             db.session.commit()


# Web routes go here
@app.route('/')
def home():
    # create_stats_table()
    return render_template("home-page.html")

# Web routes go here


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        full_name = request.form['full-name']
        email = request.form['email']
        password = request.form['password']
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            add_user(username, full_name, email, password_hash)
            flash("User successfully added")
            return redirect(url_for('login'))
        except exc.IntegrityError:
            flash("Username already exists")
            return render_template('register.html')

    else:
        return render_template("register.html")

def divide(a, b):
    if (b == 0):
        return 0
    return a/b

@app.route('/duel-result', methods=["POST"])
def duel_result():
    #input from html form
    data = json.loads(request.data)
    #sqlite3
    con = sqlite3.connect("instance/users.db")
    #players and season
    p1 = data.get("p1")
    p2 = data.get("p2")
    season = data.get("season")
    #map corresponding to columns in the database
    cols = [["gp", ["games_played"]],
            ["pts", ["points"]],
            ["reb", ["rebounds"]],
            ["ast", ["assists"]],
            ["fg_pct", ["fg_attempts", "fg_made"]],
            ["fg3_pct", ["fg3_attempts", "fg3_made"]],
            ["ft_pct", ["ft_attempts", "ft_made"]]]
    #build the SQL query
    p1_query = "SELECT year, games_played, "
    col_cnt = 0
    for pair in cols:
        if (data.get(pair[0])):
            for val in pair[1]:
                p1_query += val + ", "
            col_cnt += 1
    p1_query = p1_query[0 : len(p1_query) - 2]
    p1_query += " FROM Stats WHERE LOWER(name) == LOWER(\""
    p2_query = p1_query
    p1_query += p1 + "\")"
    p2_query += p2 + "\")"
    #execute the SQL query
    cur = con.cursor()
    p1_res = cur.execute(p1_query).fetchall()
    cur = con.cursor()
    p2_res = cur.execute(p2_query).fetchall()
    #check that the query was valid
    if (len(p1_res) == 0):
        return jsonify({"OK": False, "message": "Player 1 is not a (former) NBA player."})
    if (len(p2_res) == 0):
        return jsonify({"OK": False, "message": "Player 2 is not a (former) NBA player."})
    if (col_cnt == 0):
        return jsonify({"OK": False, "message": "Please select a non-empty set of stats."})
    if (season == "career"):
        #process the result of the query
        num1 = [0 for i in range(col_cnt)]
        num2 = [0 for i in range(col_cnt)]
        denom1 = [0 for i in range(col_cnt)]
        denom2 = [0 for i in range(col_cnt)]
        tot_games1 = 0
        tot_games2 = 0
        for tup in p1_res:
            num_col = 0
            tup_col = 2
            for pair in cols:
                if (not data.get(pair[0])):
                    continue
                if (len(pair[1]) == 1):
                    num1[num_col] += tup[tup_col]
                else:
                    num1[num_col] += tup[tup_col + 1]
                    denom1[num_col] += tup[tup_col]
                num_col += 1
                tup_col += len(pair[1])
            tot_games1 += tup[1]
        for tup in p2_res:
            num_col = 0
            tup_col = 2
            for pair in cols:
                if (not data.get(pair[0])):
                    continue
                if (len(pair[1]) == 1):
                    num2[num_col] += tup[tup_col]
                else:
                    num2[num_col] += tup[tup_col + 1]
                    denom2[num_col] += tup[tup_col]
                num_col += 1
                tup_col += len(pair[1])
            tot_games2 += tup[1]
        start = 0
        if (data.get("gp")):
            start = 1
        for i in range(start, col_cnt):
            if (denom1[i] != 0):
                num1[i] = 100*divide(num1[i], denom1[i])
            else:
                num1[i] = divide(num1[i], tot_games1)
            num1[i] = round(num1[i], 1)
        for i in range(start, col_cnt):
            if (denom2[i] != 0):
                num2[i] = 100*divide(num2[i], denom2[i])
            else:
                num2[i] = divide(num2[i], tot_games2)
            num2[i] = round(num2[i], 1)
        #return the processed result
        return jsonify({"OK": True, "stats1": num1, "stats2": num2})
    else: #season == "rookie" or season == "custom"
        if (season == "rookie"):
            season1 = min(p1_res)[0]
            season2 = min(p2_res)[0]
        else:
            season1 = int(data["season1"])
            season2 = int(data["season2"])
        #process the result of the query
        stats1 = []
        stats2 = []
        for tup in p1_res:
            if tup[0] != season1:
                continue
            tup_col = 2
            for pair in cols:
                if (not data.get(pair[0])):
                    continue
                if (pair[0] == "gp"):
                    stats1.append(tup[tup_col])
                elif (len(pair[1]) == 1):
                    stats1.append(round(divide(tup[tup_col], tup[1]), 1))
                else:
                    stats1.append(round(100*divide(tup[tup_col + 1], tup[tup_col]), 1))
                tup_col += len(pair[1])
        for tup in p2_res:
            if tup[0] != season2:
                continue
            tup_col = 2
            for pair in cols:
                if (not data.get(pair[0])):
                    continue
                if (pair[0] == "gp"):
                    stats2.append(tup[tup_col])
                elif (len(pair[1]) == 1):
                    stats2.append(round(divide(tup[tup_col], tup[1]), 1))
                else:
                    stats2.append(round(100*divide(tup[tup_col + 1], tup[tup_col]), 1))
                tup_col += len(pair[1])
        #check that the query was valid
        if (stats1 == []):
            return jsonify({"OK": False, "message": ("Player 1 did not play in the " + str(season1 - 1) + "-" + str(season1) + " season.")})
        if (stats2 == []):
            return jsonify({"OK": False, "message": ("Player 2 did not play in the " + str(season2 - 1) + "-" + str(season2) + " season.")})
        #return the processed result
        return jsonify({"OK": True, "stats1": stats1, "stats2": stats2})

@app.route('/duel')
def duel():
    return render_template("duel.html")

def toint(x):
    try:
        return int(x)
    except:
        return None

def tofloat(x):
    try:
        return float(x)
    except:
        return None

@app.route('/predict-player-result', methods=["POST"])
def hypo_player_result():
    #input from html form
    data = json.loads(request.data)
    #sqlite3
    con = sqlite3.connect("instance/users.db")
    #map corresponding to columns in the database
    cols = [["gp", ["games_played"]],
            ["pts", ["points"]],
            ["reb", ["rebounds"]],
            ["ast", ["assists"]],
            ["fg_pct", ["fg_attempts", "fg_made"]],
            ["fg3_pct", ["fg3_attempts", "fg3_made"]],
            ["ft_pct", ["ft_attempts", "ft_made"]]]
    #check that the query is valid
    data["gp"] = toint(data["gp"])
    if (data["gp"] is None or 1 > data["gp"] or data["gp"] > 82):
        return jsonify({"OK": False, "message": "Please enter an INTEGER in the RANGE [1, 82] for Games Played."})
    for pair in cols[1:]:
        data[pair[0]] = tofloat(data[pair[0]])
        if (data[pair[0]] == None or data[pair[0]] < 0):
            return jsonify({"OK": False, "message": "Please check that all Stats have been entered and they are NON-NEGATIVE NUMBERS."})
    for pair in cols[1:]:
        if (pair[0].find("pct") != -1 and data[pair[0]] > 100):
            return jsonify({"OK": False, "message": "Please check that all entered percentages are LESS THAN OR EQUAL to 100."})
    #query the SQL database
    cur = con.cursor()
    cur.execute("DROP VIEW IF EXISTS RookieSeasons")
    cur = con.cursor()
    cur.execute("CREATE VIEW RookieSeasons AS SELECT name, MIN(year), games_played as name, year, games_played FROM Stats GROUP BY name")
    cur = con.cursor()
    cur.execute("DROP VIEW IF EXISTS TargetPlayers")
    cur = con.cursor()
    cur.execute("CREATE VIEW TargetPlayers AS SELECT name FROM RookieSeasons WHERE games_played==" + str(data["gp"]))
    cur = con.cursor()
    res = cur.execute("SELECT * FROM TargetPlayers NATURAL JOIN Stats").fetchall()
    #process the results of query
    accum_stats = []
    num_players = []
    name_to_season = {}
    for tup in res:
        if (tup[0] not in name_to_season):
            name_to_season[tup[0]] = 1
        else:
            name_to_season[tup[0]] += 1
        if (name_to_season[tup[0]] > len(accum_stats)):
            accum_stats.append([0 for i in range(len(cols))])
            num_players.append(0)
        j = 0
        k = 2
        while (j < len(cols)):
            if (cols[j][0] == "gp"):
                accum_stats[name_to_season[tup[0]] - 1][j] += tup[k]
            elif (len(cols[j][1]) == 1):
                accum_stats[name_to_season[tup[0]] - 1][j] += divide(tup[k], tup[2])
            else:
                accum_stats[name_to_season[tup[0]] - 1][j] += divide(tup[k + 1], tup[k])
            k += len(cols[j][1])
            j += 1
        num_players[name_to_season[tup[0]] - 1] += 1
    avg_stats = [[] for i in range(len(accum_stats))]
    for i in range(len(accum_stats)):
        season_stats = accum_stats[i]
        for j in range(len(cols)):
            avg_stats[i].append(accum_stats[i][j]/num_players[i])
    cur_year = datetime.now().year
    predicted_stats = []
    for season in range(int(data["season"]), cur_year + 1):
        i = season - int(data["season"])
        if (num_players[i] < num_players[0]/2):
            break
        predicted_stats.append([])
        for j in range(len(cols)):
            predicted_stats[i].append(divide(data[cols[j][0]],avg_stats[0][j])*avg_stats[i][j])
            if (cols[j][0] == "GP"):
                predicted_stats[i][j] = round(predicted_stats[i][j])
                predicted_stats[i][j] = max(predicted_stats[i][j], 1)
                predicted_stats[i][j] = min(predicted_stats[i][j], 82)
            elif (len(cols[j][1]) == 1):
                predicted_stats[i][j] = round(predicted_stats[i][j], 1)
            else:
                predicted_stats[i][j] = round(predicted_stats[i][j], 1)
                predicted_stats[i][j] = min(predicted_stats[i][j], 100)
    return jsonify({"OK": True, "stats": predicted_stats})
    

@app.route('/predict-player')
def hypo_player():
    return render_template("predict-player.html")


app.run(debug=True, host='0.0.0.0', port=81)
