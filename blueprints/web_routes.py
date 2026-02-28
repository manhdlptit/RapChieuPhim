from dotenv import load_dotenv
load_dotenv()
from flask import redirect, url_for, render_template, request, session, flash, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from blueprints.model import db, User

web_route = Blueprint("web_route",__name__)

@web_route.route("/")
@web_route.route("/signup", methods = ["POST","GET"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email_user")
        name = request.form.get("user_name") 
        input_password = request.form.get("password")
        check_password = request.form.get("check_password")

        found_user_with_email= User.query.filter(User.email == email).first()
        found_user_with_name = User.query.filter(User.name == name).first()
        if found_user_with_email:
            flash ("email existed!", "error")
        if input_password != check_password:
            flash('password input different check password')
        if found_user_with_name:
            flash ("user name existed!")
        
        session["email"] = email
        password = generate_password_hash(input_password)
        new_user = User(email, name, password)
        db.session.add(new_user)
        db.session.commit()
        flash("account are created!")
        return redirect(url_for("web_route.login"))
    if "email" in session:
        session.pop("email",None)
        flash("You are logout")
    return render_template("signup.jinja")
    
    
            
@web_route.route("/login", methods = ["POST","GET"])
def login():
    if request.method == "POST":
        email_account = request.form.get("email")
        found_user_with_email = User.query.filter(User.email == email_account).first()
        if found_user_with_email:
            if check_password_hash(found_user_with_email.password, request.form.get("password")):
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

@web_route.route("/logout")
def logout():
    if "email" in session:
        session.pop("email",None)
        return redirect(url_for("web_route.login"))
    flash("You not login")
    return redirect(url_for("web_route.login"))
    
@web_route.route("/delete_user")
def delete_account():
    if "email" in session:
        email_user = session["email"]
        found_user_with_email = User.query.filter(User.email == email_user).first()
        if found_user_with_email:
            db.session.delete(found_user_with_email)
            db.session.commit()
            session.pop("email",None)
            flash("you are delete your account!")
            return redirect(url_for("web_route.login"))
    flash("you not login")
    return redirect(url_for("web_route.login"))

@web_route.route("/homepage")
def homepage():
    return render_template("homepage.html")

@web_route.route("/movie_schedule")
def movie_schedule():
    return render_template("movie_schedule.html")

@web_route.route("/promotion")
def promotion():
    return render_template("promotion.html")

@web_route.route("/new")
def new():
    return render_template("new.html")

@web_route.route("/price")
def price():
    return render_template("price.html")

@web_route.route("/intro")
def intro():
    return render_template("intro.html")

@web_route.route("/film_week")
def film_week():
    return render_template("film_week.html")
