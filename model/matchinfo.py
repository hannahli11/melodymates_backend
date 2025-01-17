from flask import current_app, request, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin
from __init__ import app, db

class MatchInfo(db.Model, UserMixin):
    __tablename__ = 'matchinfo'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), nullable=False)  # User's name
    _uid = db.Column(db.String(255), unique=True, nullable=False)  # User's unique identifier
    _favorites = db.Column(db.JSON, nullable=True)  # JSON column to store favorite artists
    _song_preferences = db.Column(db.JSON, nullable=True)  # JSON column to store song preferences

    def __init__(self, name, uid, favorites=None, song_preferences=None):
        self._name = name
        self._uid = uid
        self._favorites = favorites if favorites else []
        self._song_preferences = song_preferences if song_preferences else []

    @property
    def name(self):
        return self._name

    @property
    def uid(self):
        return self._uid

    @property
    def favorites(self):
        return self._favorites
    
    @property
    def song_preferences(self):
        return self._song_preferences

    def add_song_preference(self, song, likes):
        self._song_preferences.append({"song": song, "likes": likes})
        db.session.commit()
        return True

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def read(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'name': self.name,
            'favorites': self.favorites,
            'song_preferences': self.song_preferences,
        }

    def update(self, inputs):
        if not isinstance(inputs, dict):
            return self

        name = inputs.get("name", "")
        favorites = inputs.get("favorites", None)
        song_preferences = inputs.get("song_preferences", None)

        if name:
            self._name = name
        if favorites is not None:
            self._favorites = favorites
        if song_preferences is not None:
            self._song_preferences = song_preferences

        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Initialization function to add test data
def initMatchInfo():
    with app.app_context():
        db.create_all()
        
        # Sample test data for Carson and Rowan
        carson = MatchInfo(name='Carson', uid='carson_01', favorites=['Taylor Swift'],
                           song_preferences=[{"song": "Love Story", "likes": "Yes"},
                                             {"song": "Bad Blood", "likes": "No"}])
        
        rowan = MatchInfo(name='Rowan', uid='rowan_02', favorites=['Drake'],
                          song_preferences=[{"song": "God's Plan", "likes": "Yes"},
                                            {"song": "Hotline Bling", "likes": "No"}])
        
        users = [carson, rowan]

        for user in users:
            try:
                user.create()
                print(f"Added user {user.name} successfully.")
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error adding user {user.name}: {e}")
