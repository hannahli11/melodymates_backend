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
    
    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, genres):
        self._genres = genres

    def create(self):
        # Check if user already exists
        existing_user = ArtInfo.query.filter_by(_uid=self._uid).first()

        if existing_user:
            # Update the existing user's data
            existing_user._name = self._name
            existing_user._uid = self._uid
            existing_user._favorites = self._favorites
            db.session.commit()
            return existing_user
        else:
            # If user doesn't exist, create a new user
            db.session.add(self)
            db.session.commit()
            return self
        
    def create_or_update_art_info(data):
        uid = data.get("uid")
        artist = ArtInfo.query.filter_by(_uid=uid).first()
    
        if artist:
        # If user exists, update the record
            return artist.update(data)
        else:
        # If user doesn't exist, create a new record
            new_artist = ArtInfo(**data)
            return new_artist.create()

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
        """
        Synchronizes the provided data with the ArtInfo database.
        Updates existing records or creates new ones.
        """
        restored_records = []
        for art_data in data:
            id = art_data.get("id")  # Fetch the id from the provided data
            record = ArtInfo.query.filter_by(id=id).first()

            if record:
                # Update the existing record
                record.update(art_data)
                restored_records.append(record.read())
            else:
                # Create a new record if it doesn't exist
                try:
                    new_record = ArtInfo(
                        name=art_data.get("name"),
                        uid=art_data.get("uid"),
                        favorites=art_data.get("favorites", [])
                    )
                    new_record.create()
                    restored_records.append(new_record.read())
                except IntegrityError as e:
                    db.session.rollback()  # Rollback the session in case of any error
                    print(f"Error restoring record with uid {art_data.get('uid')}: {e}")
        return restored_records


# Initialization function to add test data
def initArtinfo():
    """
    Initializes the ArtInfo table with test data.
    """
    with app.app_context():
        db.create_all() 
        # Tester data for ArtInfo
        u1 = ArtInfo(name='Brandon Smurlo', uid='bsmurlo', favorites=['Bob Marley'])
        u2 = ArtInfo(name='Rhea Rajashekhar', uid='rhear_02', favorites=['Don Toliver'])
        artists = [u1, u2]

    for artist in artists:
            try:
                artist.create()  # Insert data into the database
                print(f"Added artist {artist.name} successfully.")
            except IntegrityError as e:
                db.session.rollback()  # Rollback the session in case of an error
                print(f"Error adding artist {artist.name}: {e}")
                