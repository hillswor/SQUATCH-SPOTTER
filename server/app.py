from flask import Flask, request, session, make_response, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_bcrypt import check_password_hash
from dotenv import load_dotenv
import os
import ipdb

from models import User, Location, Sighting, Comment
from extensions import db, migrate


# Load environment variables from .env
load_dotenv()

# Retrieve the secret key from the environment variable
secret_key = os.getenv("SECRET_KEY")


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.compact = False

    db.init_app(app)
    migrate.init_app(app, db)

    return app


app = create_app()
api = Api(app)


class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            return make_response(jsonify(user.to_dict()), 200)
        else:
            return make_response({"error": "Invalid username or password"}, 401)


api.add_resource(Login, "/login")


class UserList(Resource):
    def get(self):
        users = User.query.all()
        return [user.to_dict() for user in users]

    def post(self):
        pass


api.add_resource(UserList, "/users")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
