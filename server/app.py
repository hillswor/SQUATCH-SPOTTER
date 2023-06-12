from flask import Flask, request, session, make_response, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_bcrypt import check_password_hash, generate_password_hash
from dotenv import load_dotenv
import os
from datetime import datetime
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

    def post(self):
        data = request.get_json()
        user_id = data.get("user_id")
        location_id = data.get("location_id")
        sighting_date_string = data.get("sighting_date")
        sighting_time = data.get("sighting_time")
        description = data.get("description")

        sighting_time = datetime.strptime(sighting_time, "%H:%M").time()
        try:
            sighting_date = datetime.strptime(sighting_date_string, "%Y-%m-%d").date()
        except ValueError:
            return make_response(
                {"error": "Invalid date format. Please use 'YYYY-MM-DD'."}, 400
            )

        new_sighting = Sighting(
            user_id=user_id,
            location_id=location_id,
            sighting_date=sighting_date,
            sighting_time=sighting_time,
            description=description,
        )
        db.session.add(new_sighting)
        db.session.commit()

        return make_response(jsonify(new_sighting.to_dict()), 201)


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


class Locations(Resource):
    def get(self):
        locations = Location.query.all()
        return make_response(jsonify([location.to_dict() for location in locations]))

    def post(self):
        data = request.get_json()
        name = data.get("name")
        state = data.get("state")
        description = data.get("description")

        new_location = Location(name=name, state=state, description=description)
        db.session.add(new_location)
        db.session.commit()

        return make_response(jsonify(new_location.to_dict()), 201)


api.add_resource(Locations, "/locations")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
