from flask import current_app, request, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin
from __init__ import app, db
class MusicPref(db.Model, UserMixin):
    __tablename__ = 'musicpref'
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _favorites = db.Column(db.JSON, nullable=True)
    _music_platform = db.Column(db.String(255), nullable=True)
    _learn_preference = db.Column(db.String(255), nullable=True)
    _listening_frequency = db.Column(db.String(255), nullable=True)
    _favorite_era = db.Column(db.String(255), nullable=True)
    _important_aspect = db.Column(db.String(255), nullable=True)
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
    def create(self):
        # Check if user already exists
        existing_user = MusicPref.query.filter_by(_uid=self._uid).first()
        if existing_user:
            # Update the existing user's data
            existing_user._name = self._name
            existing_user._favorites = self._favorites
            existing_user._music_platform = self._music_platform
            existing_user._learn_preference = self._learn_preference
            existing_user._listening_frequency = self._listening_frequency
            existing_user._favorite_era = self._favorite_era
            existing_user._important_aspect = self._important_aspect
            db.session.commit()
            return existing_user
        else:
            # If user doesn't exist, create a new user
            db.session.add(self)
            db.session.commit()
            return self
    def read(self):
        """
        Return the record as a dictionary (JSON-ready).
        """
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
        """
        Update the MusicPref record in the database.
        """
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
        """
        Delete the MusicPref record from the database.
        """
        db.session.delete(self)
        db.session.commit()
# Handling GET, POST, PUT, DELETE in API
# POST - Create or Update a user
def create_or_update_music_pref(data):
    """
    Create or update a MusicPref record in the database.
    """
    uid = data.get("uid")
    user = MusicPref.query.filter_by(_uid=uid).first()
    if user:
        # If user exists, update the record
        return user.update(data)
    else:
        # If user doesn't exist, create a new record
        new_user = MusicPref(**data)
        return new_user.create()
# GET - Get a user's data
def get_music_pref(uid):
    """
    Retrieve a MusicPref record by UID.
    """
    user = MusicPref.query.filter_by(_uid=uid).first()
    if user:
        return user.read()
    else:
        return None
# PUT - Update an existing user's data
def update_music_pref(uid, data):
    """
    Update a MusicPref record by UID.
    """
    user = MusicPref.query.filter_by(_uid=uid).first()
    if user:
        return user.update(data)
    else:
        return None
# DELETE - Delete a user from the database
def delete_music_pref(uid):
    """
    Delete a MusicPref record by UID.
    """
    user = MusicPref.query.filter_by(_uid=uid).first()
    if user:
        user.delete()
        return True
    else:
        return False
# Initialize with some test data
def initMusicPref():
    """
    Initialize the database with test data.
    """
    with app.app_context():
        db.create_all()
        u1 = MusicPref(name='Brandon Smurlo', uid='brandonsmurlo_08', favorites=['Travis Scott'],
                       music_platform='Spotify', learn_preference='Social Media', listening_frequency='Weekly',
                       favorite_era='Modern', important_aspect='Vocals')
        u1.create()
# Call init function to set up database and add test users
initMusicPref()