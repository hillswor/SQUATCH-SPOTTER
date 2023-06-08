from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

from models import User, Location, Sighting, Comment
from extensions import db, migrate


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.compact = False

    db.init_app(app)
    migrate.init_app(app, db)

    return app


app = create_app()
api = Api(app)


class Home(Resource):
    def get(self):
        return {"message": "Hello, World!"}


api.add_resource(Home, "/")


class UserList(Resource):
    def get(self):
        users = User.query.all()
        return [user.to_dict() for user in users]

    def post(self):
        pass


api.add_resource(UserList, "/users")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
