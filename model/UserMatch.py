from flask import current_app, request, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin
from __init__ import app, db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # User's name
    preferences = db.Column(db.JSON, nullable=False)  # Store preferences as JSON
    bio = db.Column(db.Text, nullable=False)          # User bio

    def __init__(self, name, preferences, bio):
        self.name = name
        self.preferences = preferences
        self.bio = bio

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError as e:
            db.session.rollback()
            raise Exception(f"Error creating user: {e}")

    def read(self):
        """
        Converts the user object to a dictionary format for the API.
        """
        return {
            "id": self.id,
            "name": self.name,
            "preferences": self.preferences,
            "bio": self.bio
        }

    def update(self, data):
        """
        Updates the user's details.
        """
        if "name" in data:
            self.name = data["name"]
        if "preferences" in data:
            self.preferences = data["preferences"]
        if "bio" in data:
            self.bio = data["bio"]
        db.session.commit()
        return self

    def delete(self):
        """
        Deletes the user from the database.
        """
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_user_by_name(name):
        """
        Fetch a user by their name.
        """
        return User.query.filter_by(name=name).first()

# Initialization function to add sample data
def init_users():
    with current_app.app_context():
        db.create_all()
        # Sample users
        users = [
            User(
                name="Hannah",
                preferences={
                    "Black Star - Radiohead": "No",
                    "Sicko Mode - Travis Scott": "Yes",
                    "Bad Guy - Billie Eilish": "No",
                    "No Tears Left to Cry - Ariana Grande": "Yes",
                    "Ex-Factor - Lauryn Hill": "No"
                },
                bio="Hannah loves pop music and high-energy beats."
            ),
            User(
                name="Rhea",
                preferences={
                    "Black Star - Radiohead": "Yes",
                    "Sicko Mode - Travis Scott": "No",
                    "Bad Guy - Billie Eilish": "Yes",
                    "No Tears Left to Cry - Ariana Grande": "No",
                    "Ex-Factor - Lauryn Hill": "Yes"
                },
                bio="Rhea enjoys soulful tunes and lyrical depth."
            ),
            User(
                name="Carson",
                preferences={
                    "Black Star - Radiohead": "No",
                    "Sicko Mode - Travis Scott": "Yes",
                    "Bad Guy - Billie Eilish": "No",
                    "No Tears Left to Cry - Ariana Grande": "Yes",
                    "Ex-Factor - Lauryn Hill": "No"
                },
                bio="Carson is into upbeat tracks and modern hits."
            ),
            User(
                name="Rowan",
                preferences={
                    "Black Star - Radiohead": "Yes",
                    "Sicko Mode - Travis Scott": "No",
                    "Bad Guy - Billie Eilish": "Yes",
                    "No Tears Left to Cry - Ariana Grande": "No",
                    "Ex-Factor - Lauryn Hill": "Yes"
                },
                bio="Rowan loves alternative and indie music."
            )
        ]

        for user in users:
            try:
                user.create()
                print(f"Added user {user.name} successfully.")
            except Exception as e:
                print(f"Error adding user {user.name}: {e}")
