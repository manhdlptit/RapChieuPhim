from dotenv import load_dotenv
load_dotenv()
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user_information"
    
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

class Showtime(db.Model):
    __tablename__ = "show_time_movies"

    id = db.Column(db.Integer, primary_key = True)
    movie_id = db.Column(db.Integer, db.ForeignKey("list_movies.id"), nullable = False)
    start_time = db.Column(db.DateTime, nullable = False)
    room = db.Column(db.String(20))
    movie = db.relationship("Movies", backref=db.backref("showtimes", lazy=True))

    def __init__(self, movie_id, start_time, room):
        self.movie_id = movie_id
        self.start_time = start_time
        self.room = room
        
    