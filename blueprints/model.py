from dotenv import load_dotenv
load_dotenv()
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True)
    name = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(300))
    token = db.Column(db.String(300))

    def __init__(self, email, name, password, token = None):
        self.email = email
        self.name = name
        self.password = password
        self.token = token

class Movies(db.Model):
    __tablename__ = "list_movies"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    duration_minutes = db.Column(db.Integer)
    description = db.Column(db.String(10000))

    def __init__(self, title, duration_minutes = None, description = None):
        self.title = title
        self.duration_minutes = duration_minutes
        self.description = description