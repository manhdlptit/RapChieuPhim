from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///signin.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(), unique = True, nullable = False)
    name = db.Column(db.String(), unique = True, nullable = False)
    password = db.Column(db.String(), unique = True, nullable = False)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

# bài 1.1
# @app.route('/api/hello', methods=["GET"])
# def hello_api():
#     try:
#         return jsonify({"message": "Hello from API"})
#     except Exception as a:
#         return jsonify({"error": str(a)})

# bài 1.2
# @app.route("/api/users")
# def print_user():
#     try:
#         users = User.query.all()
#         list_users = []
#         for user in users:
#             list_users.append({
#                 "id" : user.id,
#                 "email" : user.email,
#                 "name" : user.name
#             })
#         return jsonify(list_users)
#     except Exception as a:
#         return jsonify({"error": str(a)})

# bài1.3
# @app.route("/api/users/<int:id>")
# def print_id_user(id):
#     found_id = User.query.get(id)
#     try:
#         if found_id:
#             return jsonify({
#                 "id" : found_id.id,
#                 "email" : found_id.email,
#                 "name" : found_id.name
#             })
#         return jsonify({"error": "User not found"}), 404
#     except Exception as a:
#         return jsonify({"error": str(a)})

# bài 2.1
# @app.route("/api/users", methods = ["POST"])
# def create_user():
#     data = request.get_json()

#     email = data.get("email")
#     name = data.get("name")
#     password = data.get("password")

#     if not email or not name or not password:
#         return jsonify({"error" : " Do not null any value"})

#     found_user = User.query.filter((User.email == email) | (User.name == name)).first()

#     if found_user:
#         return jsonify({"error": "Email or name already exists"}), 400
#     try:
#         new_user = User(email, name, password)
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify({"id" : new_user.id,
#                         "email" : new_user.email,
#                         "name" : new_user.name
#                         }), 201
#     except Exception as a:
#         db.session.rollback()
#         return {"error" : str(a)}

# bài 2.2 
# @app.route("/api/users/search")
# def found_user():
#     found = request.args.get("email")
#     try:
#         if found:
#             search = User.query.filter((User.email == found)).first()
#             if search:
#                 return jsonify({
#                     "id" : search.id,
#                     "name" : search.name,
#                     "email" : search.email
#                 })
#             return jsonify ({"error" : "error, not found email"}), 400
#         return jsonify ({"error" : "error, you don't input email"}), 404
#     except Exception as e:
#         return jsonify({"error" : str(e)})

# bài 3.1
# @app.route("/api/users/<int:id>", methods = ["PUT"])
# def update_user(id):
#     found_id = User.query.get(id)
#     try:
#         if found_id:
#             data = request.get_json()
#             found_name_same =  User.query.filter((data.get("name") == User.name)).first()
#             if found_name_same:
#                 return jsonify({"error" : "name existed"})
#             found_id.name = data.get("name", found_id.name)
#             db.session.commit()
#             return jsonify({
#                 "id" : found_id.id,
#                 "name" : found_id.name,
#                 "email" : found_id.email
#             }), 200
#         return jsonify({"error": "User not found"}), 404
#     except Exception as e:
#         return jsonify({"error" : str(e)})

# bài 3.2  
@app.route("/api/users/<int:id>", methods = ["DELETE"])
def delete_user(id):
    found_id = db.session.get(User, id)
    try:
        if found_id:
            db.session.delete(found_id)
            db.session.commit()
            return jsonify({"message": "User deleted"}), 200
        return jsonify ({"error": "User not found"}), 404
    except Exception as a:
        return jsonify({"error": str(a)})
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True, port=8000)