from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

class User(db.Model):
    """
    SQLAlchemy model for storing user data with music preferences and bio.
    """
    __tablename__ = 'users'  # Ensures the table is registered as 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)  # User's name
    preferences = db.Column(db.JSON, nullable=False)  # Stores Yes/No responses for songs
    bio = db.Column(db.Text, nullable=False)  # Short bio of the user

    def __init__(self, name, preferences, bio):
        self.name = name
        self.preferences = preferences
        self.bio = bio

    def create(self):
        """
        Adds the current user to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            raise Exception(f"User '{self.name}' already exists.")

    def update_preferences(self, new_preferences):
        """
        Updates user preferences (Yes/No responses).
        """
        self.preferences = new_preferences
        db.session.commit()

    
    def delete(self):
        """
        Deletes the user from the database.
        """
        db.session.delete(self)
        db.session.commit()

    def read(self):
        """
        Converts the user object to a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "preferences": self.preferences,
            "bio": self.bio
        }

    @staticmethod
    def get_user_by_name(name):
        """
        Fetch a user by their name.
        """
        return User.query.filter_by(name=name).first()

    @staticmethod
    def get_all_users():
        """
        Retrieve all users.
        """
        return [user.read() for user in User.query.all()]

# Function to initialize the database with static data
def init_users():
    with current_app.app_context():
        db.create_all()

        # Static user data initialization
        static_users = [
            {
                "name": "Hannah",
                "preferences": {
                    "Black Star - Radiohead": "No",
                    "Sicko Mode - Travis Scott": "Yes",
                    "Bad Guy - Billie Eilish": "No",
                    "No Tears Left to Cry - Ariana Grande": "Yes",
                    "Ex-Factor - Lauryn Hill": "No"
                },
                "bio": "Hannah loves pop music and high-energy beats."
            },
            {
                "name": "Rhea",
                "preferences": {
                    "Black Star - Radiohead": "Yes",
                    "Sicko Mode - Travis Scott": "No",
                    "Bad Guy - Billie Eilish": "Yes",
                    "No Tears Left to Cry - Ariana Grande": "No",
                    "Ex-Factor - Lauryn Hill": "Yes"
                },
                "bio": "Rhea enjoys soulful tunes and lyrical depth."
            },
            {
                "name": "Carson",
                "preferences": {
                    "Black Star - Radiohead": "No",
                    "Sicko Mode - Travis Scott": "Yes",
                    "Bad Guy - Billie Eilish": "No",
                    "No Tears Left to Cry - Ariana Grande": "Yes",
                    "Ex-Factor - Lauryn Hill": "No"
                },
                "bio": "Carson is into upbeat tracks and modern hits."
            },
            {
                "name": "Rowan",
                "preferences": {
                    "Black Star - Radiohead": "Yes",
                    "Sicko Mode - Travis Scott": "No",
                    "Bad Guy - Billie Eilish": "Yes",
                    "No Tears Left to Cry - Ariana Grande": "No",
                    "Ex-Factor - Lauryn Hill": "Yes"
                },
                "bio": "Rowan loves alternative and indie music."
            }
        ]

        for user_data in static_users:
            if not User.get_user_by_name(user_data["name"]):  # Avoid duplicates
                user = User(
                    name=user_data["name"],
                    preferences=user_data["preferences"],
                    bio=user_data["bio"]
                )
                try:
                    user.create()
                    print(f"Added user {user.name} successfully.")
                except Exception as e:
                    print(f"Error adding user {user.name}: {e}")
