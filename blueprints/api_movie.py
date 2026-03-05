from dotenv import load_dotenv
load_dotenv()
from flask import request, jsonify, Blueprint
from blueprints.model import db, Movies, User, Showtime
from datetime import datetime

api_movie = Blueprint("api_movie", __name__)

def get_user_from_token():
    try:
        header = request.headers.get("Authorization")
        if header and header.startswith("Bearer"):
            parts = header.split(" ")
            if len(parts) == 2:
                token = header.split(" ")[1]
                user = User.query.filter(User.token == token).first()
                if user:
                    return user
        return None
    except Exception as err:
        print(err)
        return jsonify({"error": "undetermined"}), 500

def create_movies():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}),400
        title = data.get("title")
        duration_minutes = data.get("duration_minutes")
        description = data.get("description")
        found_movie_existed = Movies.query.filter((Movies.title == title) & (Movies.duration_minutes == duration_minutes) & (Movies.description == description) & (Movies.duration_minutes != None) & (Movies.description != None)).first()
        if found_movie_existed is not None:
            return jsonify({"error" : "This film existed in db!"}), 400
        if title is None or not str(title).strip():
            return jsonify({"error": "Title is required"}), 400
        if duration_minutes is not None and duration_minutes < 0:
            return jsonify({"error" : "Time of movie must positive integer"}), 400
        movie = Movies(title, duration_minutes, description)
        db.session.add(movie)
        db.session.commit()
        return jsonify({
            "id" : movie.id,
            "title" : movie.title,
            "duration_minutes" : movie.duration_minutes,
            "description" : movie.description
        }),201
    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"error" : "undetermined"}),500

def list_movies():
    try:
        movies = Movies.query.order_by(Movies.id).all()
        list_movies = []
        for movie in movies:
            list_movies.append({
                "id" : movie.id,
                "title" : movie.title,
                "duration_minutes" : movie.duration_minutes,
                "description" : movie.description
            })
        return jsonify(list_movies),200
    except Exception as err:
        print(err)
        return jsonify({"error" : "undetermined"}),500

@api_movie.route("/", methods = ["GET", "POST"])
def call_api_movies():
    try:
        user = get_user_from_token()
        if user is None:
            return jsonify({"error": "Unauthorized"}), 401
        if request.method == "GET":
            return list_movies()
        if request.method == "POST":
            return create_movies()
    except Exception as err:
        print(err)
        return jsonify({"error" : "undetermined"}),500

def list_movies_with_id(id):
    try:
        movie = db.session.get(Movies, id)
        if movie is None:
            return jsonify({"error": "Movie not found"}), 404
        return jsonify({
            "id" : movie.id,
            "title" : movie.title,
            "duration_minutes" : movie.duration_minutes,
            "description" : movie.description
        }), 200
    except Exception as err:
        print(err)
        return jsonify({"error" : "undetermined"}),500

def update_movie(id):
    try:
        found_movies_with_id = db.session.get(Movies,id)
        if found_movies_with_id is None:
            return jsonify({"error": "Movie not found"}), 404
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}),400
        title = data.get("title", found_movies_with_id.title)
        duration_minutes = data.get("duration_minutes", found_movies_with_id.duration_minutes)
        description = data.get("description", found_movies_with_id.description)
        if not title or not str(title).strip():
            return jsonify({"error": "Title is required"}), 400
        if duration_minutes is not None and duration_minutes < 0:
            return jsonify({"error" : "Time of movie must positive integer"}), 400
        found_movies_with_id.title = title
        found_movies_with_id.duration_minutes = duration_minutes
        found_movies_with_id.description = description
        db.session.commit()
        return jsonify({
            "id" : found_movies_with_id.id,
            "title" : found_movies_with_id.title,
            "duration_minutes" : found_movies_with_id.duration_minutes,
            "description" : found_movies_with_id.description
        }),200
    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"error" : "undetermined"}),500

def delete_movie(id):
    try:
        found_id = db.session.get(Movies, id)
        if found_id is None:
            return jsonify({"error": "Movie not found"}), 404
        db.session.delete(found_id)
        db.session.commit()
        return jsonify({"message": "Movie deleted"}),200
    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"error" : "undetermined"}),500
    
@api_movie.route("/<int:id>", methods = ["GET","PUT","DELETE"])
def call_api_movie_with_id(id):
    try:
        user = get_user_from_token()
        if user is not None:
            if request.method == "GET":
                return list_movies_with_id(id)
            if request.method == "PUT":
                return update_movie(id)
            if request.method == "DELETE":
                return delete_movie(id)
        return jsonify({"error": "Unauthorized"}), 401
    except Exception as err:
        print(err)
        return jsonify({"error" : "undetermined"}),500
    
def create_showtime_for_movie(id):
    try:
        user = get_user_from_token()
        if user is None:
            return jsonify({"error": "Unauthorized"}), 401
        found_movie_with_id = db.session.get(Movies, id)
        if found_movie_with_id is None:
            return jsonify({"error": "Movie not found"}), 404
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400

        input_start_time = data.get("input_start_time")
        room = data.get("room")

        if input_start_time is None:
            return jsonify({"error" : "start_time is not Null"}), 400
        try:
            start_time = datetime.fromisoformat(input_start_time)
        except ValueError:
            return jsonify({"error" : "format of start time is ''YYYY-MM-DDTHH:MM:SS'' "}), 400
        new_showtime = Showtime(id, start_time, room)
        db.session.add(new_showtime)
        db.session.commit()
        return jsonify({
            "start_time" : new_showtime.start_time.isoformat(),
            "room" : new_showtime.room
        }), 201
    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"error" : "undetermined"}),500
    
def showtime_of_movie(id):
    try:
        user = get_user_from_token()
        if user is None:
            return jsonify({"error": "Unauthorized"}), 401
        found_movie_with_id = db.session.get(Movies, id)
        if not found_movie_with_id:
            return jsonify({"error": "Movie not found"}), 404
        list_showtime = []
        all_showtime = Showtime.query.filter(Showtime.movie_id == id).order_by(Showtime.start_time).all()
        for showtime in all_showtime:
            list_showtime.append({
                "id" : showtime.id,
                "movie_id" : showtime.movie_id,
                "start_time" : showtime.start_time.isoformat(),
                "room" : showtime.room
            })
        return jsonify(list_showtime), 200
    except Exception as err:
        print(err)
        return jsonify({"error" : "undetermined"}),500
    
@api_movie.route("/<int:id>/showtime", methods = ["POST","GET"])
def call_showtime_with_id(id):
    try:
        user = get_user_from_token()
        if user is None:
            return jsonify({"error": "Unauthorized"}), 401
        if request.method == "POST":
            return create_showtime_for_movie(id)
        if request.method == "GET":
            return showtime_of_movie(id)
    except Exception as err:
        print(err)
        return jsonify({"error" : "undetermined"}),500
    
def update_showtime_with_id(id):
    try:
        user = get_user_from_token()
        if user is None:
            return jsonify({"error": "Unauthorized"}), 401
        found_showtime_with_id = db.session.get(Showtime, id)
        if found_showtime_with_id is None:
            return jsonify({"error": "Movie not found"}), 404
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400

        input_start_time = data.get("input_start_time", found_showtime_with_id.start_time.isoformat())
        room = data.get("room", found_showtime_with_id.room)
        movie_id = data.get("movie_id", found_showtime_with_id.movie_id)

        if input_start_time is None:
            return jsonify({"error" : "start_time is not Null"}), 400
        try:
            start_time = datetime.fromisoformat(input_start_time)
        except ValueError:
            return jsonify({"error" : "format of start time is ''YYYY-MM-DDTHH:MM:SS'' "}), 400
        found_movie_with_id = db.session.get(Movies, movie_id)
        if found_movie_with_id is None:
            return jsonify({"error" : "id in 'movie_id' is not existed"}), 404
        found_showtime_with_id.start_time = start_time
        found_showtime_with_id.room = room
        found_showtime_with_id.movie_id = movie_id
        db.session.commit()
        return jsonify({
            "start_time" : found_showtime_with_id.start_time.isoformat(),
            "room" : found_showtime_with_id.room,
            "movie_id" : found_showtime_with_id.movie_id
        }), 200
    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"error" : "undetermined"}),500
    
def showtime_with_id(id):
    try:
        user = get_user_from_token()
        if user is None:
            return jsonify({"error": "Unauthorized"}), 401
        found_id_in_Showtime = db.session.get(Showtime, id)
        if found_id_in_Showtime is None:
            return jsonify({"error": "Showtime not found"}), 404
        return jsonify({
            "id" : found_id_in_Showtime.id,
            "movie_id" : found_id_in_Showtime.movie_id,
            "start_time" : found_id_in_Showtime.start_time.isoformat(),
            "room" : found_id_in_Showtime.room
        }), 200
    except Exception as err:
        print(err)
        return jsonify({"error" : "undetermined"}),500
    
def delete_showtime_with_id(id):
    try:
        user = get_user_from_token()
        if user is None:
            return jsonify({"error": "Unauthorized"}), 401
        found_id_in_Showtime = db.session.get(Showtime, id)
        if found_id_in_Showtime is None:
            return jsonify({"error": "Showtime not found"}), 404
        db.session.delete(found_id_in_Showtime)
        db.session.commit()
        return jsonify({"message": "Showtime deleted"}), 200
    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"error" : "undetermined"}),500

@api_movie.route("/api/showtime/<int:id>", methods = ["PUT", "GET", "DELETE"])
def call_api_showtime_with_id(id):
    try:
        user = get_user_from_token()
        if user is None:
            return jsonify({"error": "Unauthorized"}), 401
        if request.method == "GET":
            return showtime_with_id(id)
        if request.method == "PUT":
            return update_showtime_with_id(id)
        if request.method == "DELETE":
            return delete_showtime_with_id(id)
    except Exception as err:
        print(err)
        return jsonify({"error" : "undetermined"}),500