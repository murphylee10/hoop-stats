from flask import Flask, render_template, request
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


with app.app_context():
    db.create_all()


def add_user(user_name, full_name, email, password):
    new_user = User(user_name=user_name, full_name=full_name,
                    email=email, password=password)
    db.session.add(new_user)
    db.session.commit()


# DB routes (methods) go here


# Web routes go here
@app.route('/')
def home():
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
