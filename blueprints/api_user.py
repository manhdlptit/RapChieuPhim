from dotenv import load_dotenv
load_dotenv()
from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from blueprints.model import db, User

api_user = Blueprint("api_user", __name__)

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

def print_user():
    try:
        users = User.query.all()
        list_users = []
        for user in users:
            list_users.append({
                "id" : user.id,
                "email" : user.email,
                "name" : user.name
            })
        return jsonify(list_users)
    except Exception as err:
        print(err)
        return jsonify({"error": "undetermined"}), 500
    
def create_user():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}),400
        email = data.get("email")
        name = data.get("name")
        input_password = data.get("password")

        if not email or not name or not input_password:
            return jsonify({"error" : " Do not null any value"}), 400
        if len(input_password) < 8:
            return jsonify({"error" : "password length is longer than 8 characters"}), 400
        found_user_with_email_and_name = User.query.filter((User.email == email) | (User.name == name)).first()
        if found_user_with_email_and_name:
            return jsonify({"error": "Email or name already exists"}), 400
        password = generate_password_hash(input_password)
        new_user = User(email, name, password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"id" : new_user.id,
                        "email" : new_user.email,
                        "name" : new_user.name
                        }), 201 
    except Exception as err:
        db.session.rollback()            
        print(err)
        return jsonify({"error" : "undetermined"}),500
    
@api_user.route("/api/users", methods = ["POST", "GET"])
def call_api_users():
    try:
        user = get_user_from_token()
        if user is None:
            return jsonify({"error":"You must create account before this update or already login or you must input correct token!"}), 401
        if request.method == "GET":
            return print_user()
        if request.method == "POST":
            return create_user()
    except Exception as err:
        print(err)
        return jsonify({"error": "undetermined"}), 500

@api_user.route("/api/logout", methods = ["POST"])
def logout_with_token():
    try:
        user = get_user_from_token()
        if user is None:
            return jsonify({"error": "Unauthorized (Maybe you input token wrong)"}), 401 # use 401
        user.token = None
        db.session.commit()
        return jsonify({"message": "Logged out"}), 200
    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"error": "undetermined"}),500
    
@api_user.route('/api/hello', methods=["GET"])
def hello_api():
    try:
        return jsonify({"message": "Hello from API"}), 200
    except Exception as err:
        print(err)
        return jsonify({"error": "undetermined"}),500
    
def print_id_user(id):
    try:
        found_user_with_id = db.session.get(User, id)
        if found_user_with_id:
            return jsonify({
                "id" : found_user_with_id.id,
                "email" : found_user_with_id.email,
                "name" : found_user_with_id.name
            })
        return jsonify({"error": "User not found"}), 404
    except Exception as err:
        print(err)
        return jsonify({"error": "undetermined"})
    
def update_user(id):
    try:
        found_user_with_id = db.session.get(User, id)
        if not found_user_with_id:
            return jsonify({"error": "User not found"}), 404
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400
        name = data.get("name")
        if not name:
            return jsonify({"error":"You have not input name"}),400
        found_name_same =  User.query.filter((User.name==name)).first()
        if name == found_user_with_id.name:
            return jsonify({"error":"This name is current your name"}), 400
        if found_name_same:
            return jsonify({"error" : "name existed"}), 400
        found_user_with_id.name = name
        db.session.commit()
        return jsonify({ 
            "id" : found_user_with_id.id,
            "name" : found_user_with_id.name,
            "email" : found_user_with_id.email
        }), 200
    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"error" : "undetermined"}),500
    
def delete_user(id):
    try:
        found_user_with_id = db.session.get(User, id)
        if not found_user_with_id:
            return jsonify({"error": "User not found"}), 404
        db.session.delete(found_user_with_id)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200
    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"error": "undetermined"}),500

@api_user.route("/api/users/<int:id>", methods = ["PUT","GET","DELETE"])
def call_api_users_with_id(id):
    try:
        user = get_user_from_token()
        if user is None:
            return jsonify({"error": "Unauthorized"}), 401
        if user.id != id:
            return jsonify({"error": "Forbidden"}), 403
        if request.method == "GET":
            return print_id_user(id)
        if request.method == "PUT":
            return update_user(id)
        if request.method == "DELETE":
            return delete_user(id)
    except Exception as err:
        print(err)
        return jsonify({"error": "undetermined"}),500

@api_user.route("/api/users/search")
def found_user():
    try:
        found_email_in_url = request.args.get("email")
        if not found_email_in_url:
            return jsonify({"error" : "error, you have not input email"}), 400 # user have not email in url
        found_user_with_email = User.query.filter((User.email == found_email_in_url)).first()
        if not found_user_with_email:
            return jsonify({"error" : "error, not found email"}), 404 #do not found email
        return jsonify({
            "id" :found_user_with_email.id,
            "name" : found_user_with_email.name,
            "email" : found_user_with_email.email
        }), 200
    except Exception as err:
        print(err)
        return jsonify({"error" : "undetermined"}),500
    
@api_user.route("/api/login", methods = ["POST"])
def create_token():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error":"Invalid JSON"}),400
        email = data.get("email")
        input_password = data.get("password")
    
        user = User.query.filter(User.email == email).first()
        if not user:
            return jsonify({"error": "Invalid password or email"}),401
        if not check_password_hash(user.password, input_password):
            return jsonify({"error": "Invalid password or email"}),401
        user.token = uuid.uuid4().hex
        db.session.commit()
        return jsonify({
            "token": user.token,
                "user":{
                    "id" : user.id,
                    "name" : user.name,
                    "email" : user.email
                }
        }),200
    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"error" : "undetermined"}),500

@api_user.route("/api/me")
def token_to_user():
    try:
        user = get_user_from_token()
        if user is  None:
            return jsonify({"error": "Unauthorized"}), 401
        return jsonify({
            "id" : user.id,
            "name" : user.name,
            "email" : user.email
        }),200
    except Exception as err:
        print(err)
        return jsonify({"error" : "undetermined"}),500