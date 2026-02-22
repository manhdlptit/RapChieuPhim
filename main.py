from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)

app.config["SECRET_KEY"] = 'manhdl'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///signin.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True)
    name = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(150))
    token = db.Column(db.String())

    def __init__(self, email, name, password, token = None):
        self.email = email
        self.name = name
        self.password = password
        self.token = token

@app.route("/")
@app.route("/signup", methods = ["POST","GET"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email_user")
        name = request.form.get("user_name") 
        password = request.form.get("password")
        check_password = request.form.get("check_password")
        
        session["email"] = email

        found_user = User.query.filter_by(email = email).first()
        found_email = User.query.filter_by(name = name).first()
        if found_user:
            flash ("email existed!", "error")
        elif password != check_password:
            flash('password different check password')
        elif found_email:
            flash ("user name existed!")
        else:
            new_user = User(email, name, password)
            db.session.add(new_user)
            db.session.commit()
            flash("account are created!")
            return redirect(url_for("login"))
    if "email" in session:
        session.pop("email",None)
        flash("You are logout")
    return render_template("signup.jinja")
            
@app.route("/login", methods = ["POST","GET"])
def login():
    if request.method == "POST":
        email_account = request.form["email"]
        found_email = User.query.filter_by(email = email_account).first()
        if found_email:
            if request.form["password"] == found_email.password:
                session["email"] = email_account
                flash("login successfully!")
                return render_template("home.jinja")
            flash('wrong password')
            return render_template("login.jinja")
        flash('not exist email!')
        return render_template("login.jinja")
    if "email" in session:
        flash("You login before")
        return render_template("home.jinja")
    return render_template("login.jinja")

@app.route("/logout")
def logout():
    if "email" in session:
        session.pop("email",None)
        return redirect(url_for("login"))
    flash("You not login")
    return redirect(url_for("login"))
    
@app.route("/delete_user")
def delete_account():
    if "email" in session:
        email_user = session["email"]
        found_email = User.query.filter_by(email = email_user).first()
        if found_email:
            db.session.delete(found_email)
            db.session.commit()
            session.pop("email",None)
            flash("you are delete your account!")
            return redirect(url_for("login"))
    flash("you not login")
    return redirect(url_for("login"))

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/movie_schedule")
def movie_schedule():
    return render_template("movie_schedule.html")

@app.route("/promotion")
def promotion():
    return render_template("promotion.html")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/price")
def price():
    return render_template("price.html")

@app.route("/intro")
def intro():
    return render_template("intro.html")

@app.route("/film_week")
def film_week():
    return render_template("film_week.html")

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
    except Exception as a:
        return jsonify({"error": str(a)})
    
def create_user():
    data = request.get_json()

    email = data.get("email")
    name = data.get("name")
    password = data.get("password")

    if not email or not name or not password:
        return jsonify({"error" : " Do not null any value"}), 400
    if len(password) < 8:
        return jsonify({"error" : "password length is longer than 8 characters"}), 400

    found_user = User.query.filter((User.email == email) | (User.name == name)).first()

    if found_user:
        return jsonify({"error": "Email or name already exists"}), 400
    try:
        new_user = User(email, name, password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"id" : new_user.id,
                        "email" : new_user.email,
                        "name" : new_user.name
                        }), 201
    except Exception as a:
        db.session.rollback()
        return {"error" : str(a)}
    
def get_user_from_token():
    header = request.headers.get("Authorization")
    if header and header.startswith("Bearer"):
        token = header.split(" ")[1]
        user = User.query.filter(User.token == token).first()
        if user:
            return user
        return None
    return None

@app.route("/api/logout", methods = ["POST"])
def logout_with_token():
    user = get_user_from_token()
    if user is not None:
        user.token = None
        db.session.commit()
        return jsonify({"message": "Logged out"}), 200
    return jsonify({"error": "Unauthorized (Maybe you input token wrong)"}), 401 # use 401


@app.route('/api/hello', methods=["GET"])
def hello_api():
    try:
        return jsonify({"message": "Hello from API"}), 200
    except Exception as a:
        return jsonify({"error": str(a)})

@app.route("/api/users", methods = ["POST", "GET"])
def call_api_users():
    if request.method == "GET":
        return print_user()
    if request.method == "POST":
        user = get_user_from_token()
        if user is not None:
            return create_user()
        return jsonify({"error":"You must create account before this update or already login or you must input correct token!"}), 401
    
def print_id_user(id):
    found_id = db.session.get(User, id)
    try:
        if found_id:
            return jsonify({
                "id" : found_id.id,
                "email" : found_id.email,
                "name" : found_id.name
            })
        return jsonify({"error": "User not found"}), 404
    except Exception as a:
        return jsonify({"error": str(a)})
    
def update_user(id):
    found_id = db.session.get(User, id)
    try:
        if found_id:
            data = request.get_json()
            name = data.get("name")
            if name:
                found_name_same =  User.query.filter((User.name==name)).first()
                if found_name_same:
                    return jsonify({"error" : "name existed"}), 400
                else:
                        found_id.name = name
                        db.session.commit()
                        return jsonify({ 
                            "id" : found_id.id,
                            "name" : found_id.name,
                            "email" : found_id.email
                        }), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error" : str(e)})
    
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
    


@app.route("/api/users/<int:id>", methods = ["PUT","GET","DELETE"])
def call_api_users_with_id(id):
    user = get_user_from_token()
    if user is None:
        return jsonify({"error": "Unauthorized"}), 401
    if user.id != id:
        return jsonify({"error": "Forbidden"}), 403
    if user is not None:
        if request.method == "GET":
            return print_id_user(id)
        elif request.method == "PUT":
            return update_user(id)
        elif request.method == "DELETE":
            return delete_user(id)
    
@app.route("/api/users/search")
def found_user():
    found = request.args.get("email")
    try:
        if found:
            search = User.query.filter((User.email == found)).first()
            if search:
                return jsonify({
                    "id" : search.id,
                    "name" : search.name,
                    "email" : search.email
                })
            return jsonify ({"error" : "error, not found email"}), 400
        return jsonify ({"error" : "error, you have not input email"}), 404
    except Exception as e:
        return jsonify({"error" : str(e)})
    
@app.route("/api/login", methods = ["POST"])
def create_token():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    user = User.query.filter(User.email == email).first()
    if user:
        if user.password == password:
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
        return jsonify({"error": "Invalid password"}),401
    return jsonify({"error": "Invalid email"}),401

@app.route("/api/me")
def token_to_user():
    user = get_user_from_token()
    if user is not None:
        return jsonify({
            "id" : user.id,
            "name" : user.name,
            "email" : user.email
        }),200
    return jsonify({"error": "Unauthorized"}), 401


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)