from dotenv import load_dotenv
load_dotenv()
from flask import Flask
import os
from blueprints.api_movie import api_movie
from blueprints.api_user import api_user
from blueprints.model import db
from blueprints.web_routes import web_route

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", 'default')
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///signin.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(api_movie, url_prefix = '/api/movies')
app.register_blueprint(api_user, url_prefix = '/api/users')
app.register_blueprint(web_route)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=2000)