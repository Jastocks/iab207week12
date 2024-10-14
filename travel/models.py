from . import db
from datetime import datetime
from flask_login import UserMixin

class Destination(db.Model):
    __tablename__ = 'destination'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    currency = db.Column(db.String(3))
    comments = db.relationship('Comment', backref='destination')

    def __repr__(self):
        return f"Name: {self.name}"

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    #password shoudld never be stored in the DB, only encrypted password
    #the storage should be at least 255 char long depending on your hashing algorithm
    password_hash = db.Column(db.String(255), nullable=False)
    #relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')

    def __repr__(self):
        return f"Name: {self.name}"


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    #foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'))

    def __repr__(self):
        return f"Comment: {self.text}"