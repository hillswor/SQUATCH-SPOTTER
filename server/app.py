from flask import Flask, request, session, make_response, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_bcrypt import check_password_hash, generate_password_hash
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


class CheckSession(Resource):
    def get(self):
        if session.get("user_id"):
            user = User.query.get(session["user_id"])
            return make_response(jsonify(user.to_dict()), 200)
        else:
            return make_response({"error": "No user logged in"}, 401)


api.add_resource(CheckSession, "/check-session")


class Logout(Resource):
    def delete(self):
        session.clear()
        return make_response({"message": "Successfully logged out"}, 200)


api.add_resource(Logout, "/logout")


class Users(Resource):
    def get(self):
        users = User.query.all()
        return [user.to_dict() for user in users]

    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        new_user = User(email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        return make_response(jsonify(new_user.to_dict()), 201)


api.add_resource(Users, "/users")


class Sightings(Resource):
    def get(self):
        sightings = Sighting.query.all()
        return make_response(jsonify([sighting.to_dict() for sighting in sightings]))


api.add_resource(Sightings, "/sightings")


class SightingByID(Resource):
    def get(self, id):
        sighting = Sighting.query.get(id)
        return make_response(jsonify(sighting.to_dict()))


api.add_resource(SightingByID, "/sightings/<int:id>")


class Comments(Resource):
    def post(self):
        data = request.get_json()
        user_id = data.get("user_id")
        sighting_id = data.get("sighting_id")
        comment_text = data.get("comment_text")

        new_comment = Comment(
            user_id=user_id,
            sighting_id=sighting_id,
            comment_text=comment_text,
        )
        db.session.add(new_comment)
        db.session.commit()

        return make_response(jsonify(new_comment.to_dict()), 201)


api.add_resource(Comments, "/comments")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
