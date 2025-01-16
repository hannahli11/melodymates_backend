from flask import current_app, request, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin
from __init__ import app, db



class ArtInfo(db.Model, UserMixin):
    __tablename__ = 'artinfo'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), nullable=False)  # User's name
    _uid = db.Column(db.String(255), unique=True, nullable=False)  # User's unique identifier
    _favorites = db.Column(db.JSON, nullable=True)  # JSON column to store favorite artists

    def __init__(self, name, uid, favorites=None):
        self._name = name
        self._uid = uid
        self._favorites = favorites if favorites else []

    @property
    def name(self):
        return self._name

    @property
    def uid(self):
        return self._uid

    @property
    def favorites(self):
        return self._favorites

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
        }

    def update(self, inputs):
        if not isinstance(inputs, dict):
            return self

        name = inputs.get("name", "")
        favorites = inputs.get("favorites", None)

        if name:
            self._name = name
        if favorites is not None:
            self._favorites = favorites

        db.session.commit()
        return self

        def delete(self):
            db.session.delete(self)
            db.session.commit()
    
    @staticmethod
    def restore(data):
        artists = {}
        for ArtInfo_data in data:
            id = ArtInfo_data.get("id")
            comment = ArtInfo.query.filter_by(id=id).first()
            if comment:
                comment.update(ArtInfo_data)
            else:
                print(ArtInfo_data)
                artist = ArtInfo(ArtInfo_data.get("id"), ArtInfo_data.get("uid"), ArtInfo_data.get("name"), ArtInfo_data.get("favorites"))
                artist.create()
        return artists


# Initialization function to add test data
def initArtinfo():
    """
    Initializes the ArtInfo table with test data.
    """
    with app.app_context():
        db.create_all() 
        # Tester data for ArtInfo
        u1 = ArtInfo(name='Hannah Li', uid='hannahli_11', favorites=['Travis Scott', 'Metro Boomin'])
        u2 = ArtInfo(name='Brandon Smurlo', uid='bsmurlo', favorites=['Bob Marley'])
        u3 = ArtInfo(name='Rhea Rajashakhar', uid='rhear_02', favorites=['Don Toliver'])
        artists = [u1, u2, u3]

    for artist in artists:
            try:
                artist.create()  # Insert data into the database
                print(f"Added artist {artist.name} successfully.")
            except IntegrityError as e:
                db.session.rollback()  # Rollback the session in case of an error
                print(f"Error adding artist {artist.name}: {e}")
                