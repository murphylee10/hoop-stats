from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'dkf3sldkjfDF23fLJ3b'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


app.run(debug=True, host='0.0.0.0', port=81)
