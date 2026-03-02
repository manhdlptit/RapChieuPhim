from dotenv import load_dotenv
load_dotenv()
from flask import request, jsonify, Blueprint
from blueprints.model import db, Movies, User

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

@api_movie.route("/api/movies", methods = ["GET", "POST"])
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
    
@api_movie.route("/api/movies/<int:id>", methods = ["GET","PUT","DELETE"])
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