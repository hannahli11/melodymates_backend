# db_init.py

from flask import current_app
from flask_login import UserMixin
from sqlalchemy.exc import IntegrityError
from __init__ import app, db
import os


class PublicProfile(db.Model, UserMixin):
    """
    User Model

    This class represents the User model, which is used to manage actions in the 'publicprofile' table of the database.
    It is an implementation of Object Relational Mapping (ORM) using SQLAlchemy, allowing for easy interaction
    with the database using Python code. The PublicProfile model includes various fields and methods to support user
    management and profile management functionalities.

    Attributes:
        id (Column): The primary key, an integer representing the unique identifier for the user.
        _name (Column): A string representing the user's name. It is not unique and cannot be null.
        _uid (Column): A unique string identifier for the user, cannot be null.
        _pfp (Column): A string representing the path to the user's profile picture. It can be null.
        _bio (Column): A string representing the user's bio. It can be null.
        _favorite_artist (Column): A string representing the user's favorite artist. It can be null.
    """
    __tablename__ = 'publicprofile'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _pfp = db.Column(db.String(255), unique=False, nullable=True)
    _bio = db.Column(db.String(255), unique=False, nullable=True)
    _favorite_artist = db.Column(db.String(255), unique=False, nullable=True)

    def __init__(self, name, uid, pfp='', bio='', favorite_artist=''):
        self._name = name
        self._uid = uid
        self._pfp = pfp
        self._bio = bio
        self._favorite_artist = favorite_artist

    @property
    def bio(self):
        return self._bio

    @bio.setter
    def bio(self, bio):
        self._bio = bio

    @property
    def favorite_artist(self):
        return self._favorite_artist

    @favorite_artist.setter
    def favorite_artist(self, favorite_artist):
        self._favorite_artist = favorite_artist

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        self._uid = uid

    @property
    def pfp(self):
        return self._pfp

    @pfp.setter
    def pfp(self, pfp):
        self._pfp = pfp

    def __str__(self):
        return f"PublicProfile({self._name}, {self._uid}, {self._pfp}, {self._bio}, {self._favorite_artist})"

    def create(self):
        """Add this user object to the database"""
        db.session.add(self)
        db.session.commit()

    def update(self, inputs):
        """Update the user object with new data"""
        for key, value in inputs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        """Delete the user object from the database"""
        db.session.delete(self)
        db.session.commit()


def initPublicProfile():
    """
    Initializes the database and adds initial tester data to the 'publicprofile' table.
    This function is used to populate the 'publicprofile' table with sample data.

    Uses:
        db.create_all() to create the necessary tables.
        User objects are created with sample data and added to the database.
    """
    with app.app_context():
        # Create the database and tables if they don't exist
        db.create_all()

        # Create some sample users
        u1 = PublicProfile(name='Gaheera Babbar', uid='admin_user', pfp='toby.png', bio='DNHS San Diego California.', favorite_artist='The Weeknd, Don Toliver, Ariana Grande')
        u2 = PublicProfile(name='Rowan Sutherland', uid='default_user', pfp='hop.png', bio='Computer science pioneer.', favorite_artist='Hozier, Imogen Heap, Big Thief')
        u3 = PublicProfile(name='Hannah Li', uid='niko', pfp='niko.png', bio='Music enthusiast and aspiring songwriter.', favorite_artist='Gracie Abrams, Don Toliver, Ariana Grande')

        # Add users to a list
        users = [u1, u2, u3]

        # Try to insert users into the database
        for user in users:
            try:
                user.create()
                print(f"User {user._name} created successfully.")
            except IntegrityError:
                db.session.rollback()
                print(f"Error or duplicate entry: {user._uid}")

