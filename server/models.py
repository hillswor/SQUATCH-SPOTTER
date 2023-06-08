from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(length=254), unique=True, nullable=False)
    password = db.Column(db.String(length=254))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    sightings = db.relationship("Sighting", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)
    locations = association_proxy("sightings", "location")

    @validates("email")
    def validate_email(self, key, email):
        assert (
            re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)
            is not None
        ), "Invalid email address"
        return email

    def set_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.password = hashed_password.decode("utf-8")

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat(),
        }

    def __repr__(self):
        return f"<User email={self.email}>"


class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254))
    latitude = db.Column(db.Numeric(9, 6))
    longitude = db.Column(db.Numeric(9, 6))
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    sightings = db.relationship("Sighting", backref="location", lazy=True)
    users = association_proxy("sightings", "user")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "latitude": float(self.latitude) if self.latitude is not None else None,
            "longitude": float(self.longitude) if self.longitude is not None else None,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<Location name={self.name} description={self.description}>"


class Sighting(db.Model):
    __tablename__ = "sightings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    sighting_date = db.Column(db.Date)
    sighting_time = db.Column(db.Time)
    description = db.Column(db.String(1500))
    image = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    comments = db.relationship("Comment", backref="sighting", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "location_id": self.location_id,
            "sighting_date": self.sighting_date.isoformat(),
            "sighting_time": self.sighting_time.isoformat(),
            "description": self.description,
            "image": self.get_image_base64() if self.image else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def get_image_base64(self):
        return base64.b64encode(self.image).decode("utf-8")

    def __repr__(self):
        return f"<Sighting id={self.id} user_id={self.user_id} location_id={self.location_id} sighting_date={self.sighting_date}>"


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    sighting_id = db.Column(db.Integer, db.ForeignKey("sighting.id"))
    comment_text = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "sighting_id": self.sighting_id,
            "comment_text": self.comment_text,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<Comment id={self.id} user_id={self.user_id} sighting_id={self.sighting_id}>"
