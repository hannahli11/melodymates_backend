from flask import current_app, request, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin
from __init__ import app, db


class MusicPref(db.Model, UserMixin):
    __tablename__ = 'musicpref'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), nullable=False)  # User's name
    _uid = db.Column(db.String(255), unique=True, nullable=False)  # User's unique identifier
    _favorites = db.Column(db.JSON, nullable=True)  # JSON column to store favorite artists
    _music_platform = db.Column(db.String(255), nullable=True)  # Favorite music platform
    _learn_preference = db.Column(db.String(255), nullable=True)  # How they learn about music
    _listening_frequency = db.Column(db.String(255), nullable=True)  # Listening frequency
    _favorite_era = db.Column(db.String(255), nullable=True)  # Favorite era of music
    _important_aspect = db.Column(db.String(255), nullable=True)  # Most important aspect of music

    def __init__(self, name, uid, favorites=None, music_platform=None, learn_preference=None, 
                 listening_frequency=None, favorite_era=None, important_aspect=None):
        self._name = name
        self._uid = uid
        self._favorites = favorites if favorites else []
        self._music_platform = music_platform
        self._learn_preference = learn_preference
        self._listening_frequency = listening_frequency
        self._favorite_era = favorite_era
        self._important_aspect = important_aspect

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
    def music_platform(self):
        return self._music_platform

    @property
    def learn_preference(self):
        return self._learn_preference

    @property
    def listening_frequency(self):
        return self._listening_frequency

    @property
    def favorite_era(self):
        return self._favorite_era

    @property
    def important_aspect(self):
        return self._important_aspect

    def add_favorite(self, artist_name):
        if artist_name not in self._favorites:
            self._favorites.append(artist_name)
            db.session.commit()
            return True
        return False

    def remove_favorite(self, artist_name):
        if artist_name in self._favorites:
            self._favorites.remove(artist_name)
            db.session.commit()
            return True
        return False

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
            'music_platform': self.music_platform,
            'learn_preference': self.learn_preference,
            'listening_frequency': self.listening_frequency,
            'favorite_era': self.favorite_era,
            'important_aspect': self.important_aspect,
        }

    def update(self, inputs):
        if not isinstance(inputs, dict):
            return self

        self._name = inputs.get("name", self._name)
        self._favorites = inputs.get("favorites", self._favorites)
        self._music_platform = inputs.get("music_platform", self._music_platform)
        self._learn_preference = inputs.get("learn_preference", self._learn_preference)
        self._listening_frequency = inputs.get("listening_frequency", self._listening_frequency)
        self._favorite_era = inputs.get("favorite_era", self._favorite_era)
        self._important_aspect = inputs.get("important_aspect", self._important_aspect)

        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()


# Initialization function to add test data
def initMusicPref():
    with app.app_context():
        db.create_all()
        u1 = MusicPref(name='Hannah Li', uid='hannahli_11', favorites=['Travis Scott'], 
                       music_platform='Spotify', learn_preference='Social Media', 
                       listening_frequency='Daily', favorite_era='2000s', important_aspect='Lyrics')
        u2 = MusicPref(name='Brandon Smurlo', uid='bsmurlo', favorites=['Bob Marley'], 
                       music_platform='Apple Music', learn_preference='Friends', 
                       listening_frequency='Weekly', favorite_era='70s', important_aspect='Melody')

        for user in [u1, u2]:
            try:
                user.create()
                print(f"Added user {user.name} successfully.")
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error adding user {user.name}: {e}")
