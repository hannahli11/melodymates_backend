from flask import current_app, request, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin
from model.user import User  # Assuming ArtInfo is defined in model/user.py
from __init__ import app, db

class ArtInfo(db.Model, UserMixin):
    __tablename__ = 'artinfo'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _role = db.Column(db.String(20), default="User", nullable=False)
    _favorites = db.Column(db.JSON, nullable=True)  # JSON column to store favorite artists

    def __init__(self, name, uid, role="User", favorites=None):
        self._name = name
        self._uid = uid
        self._role = role
        self._favorites = favorites if favorites else []

    @property
    def name(self):
        return self._name

    @property
    def uid(self):
        return self._uid

    @property
    def role(self):
        return self._role

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
            'role': self._role,
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

# API to get artist info by UID
@app.route('/artinfo/<string:uid>', methods=['GET'])
def get_art_info(uid):
    artist = ArtInfo.query.filter_by(_uid=uid).first()
    if artist:
        return jsonify({
            'message': 'Artist found',
            'artist': artist.read()
        })
    else:
        return jsonify({'message': 'Artist not found'}), 404

# API to create a new artist
@app.route('/artinfo', methods=['POST'])
def create_art_info():
    data = request.get_json()
    name = data.get('name')
    uid = data.get('uid')

    if not name or not uid:
        return jsonify({'message': 'Name and UID are required'}), 400

    artist = ArtInfo(name=name, uid=uid)
    result = artist.create()
    if result:
        return jsonify({
            'message': 'Artist created successfully',
            'artist': artist.read()
        }), 201
    else:
        return jsonify({'message': 'Failed to create artist'}), 400

# API to update artist info by UID
@app.route('/artinfo/<string:uid>', methods=['PUT'])
def update_art_info(uid):
    data = request.get_json()
    name = data.get('name')
    favorites = data.get('favorites')

    artist = ArtInfo.query.filter_by(_uid=uid).first()
    if artist:
        update_data = {}
        if name:
            update_data['name'] = name
        if favorites is not None:
            update_data['favorites'] = favorites

        artist.update(update_data)
        return jsonify({
            'message': 'Artist updated successfully',
            'artist': artist.read()
        })
    else:
        return jsonify({'message': 'Artist not found'}), 404

# API to delete an artist by UID
@app.route('/artinfo/<string:uid>', methods=['DELETE'])
def delete_art_info(uid):
    artist = ArtInfo.query.filter_by(_uid=uid).first()
    if artist:
        artist.delete()
        return jsonify({'message': 'Artist deleted successfully'})
    else:
        return jsonify({'message': 'Artist not found'}), 404

# API to add an artist to favorites
@app.route('/artinfo/favorites', methods=['POST'])
def add_to_favorites():
    data = request.get_json()
    uid = data.get('uid')
    artist_name = data.get('name')

    if not uid or not artist_name:
        return jsonify({'message': 'UID and artist name are required'}), 400

    artist = ArtInfo.query.filter_by(_uid=uid).first()
    if artist:
        if artist.add_favorite(artist_name):
            return jsonify({
                'message': f'Artist "{artist_name}" added to favorites',
                'favorites': artist.favorites
            })
        else:
            return jsonify({'message': 'Artist already in favorites'}), 400
    else:
        return jsonify({'message': 'Artist not found'}), 404

# API to remove an artist from favorites
@app.route('/artinfo/favorites', methods=['DELETE'])
def remove_from_favorites():
    data = request.get_json()
    uid = data.get('uid')
    artist_name = data.get('name')

    if not uid or not artist_name:
        return jsonify({'message': 'UID and artist name are required'}), 400

    artist = ArtInfo.query.filter_by(_uid=uid).first()
    if artist:
        if artist.remove_favorite(artist_name):
            return jsonify({
                'message': f'Artist "{artist_name}" removed from favorites',
                'favorites': artist.favorites
            })
        else:
            return jsonify({'message': 'Artist not found in favorites'}), 400
    else:
        return jsonify({'message': 'Artist not found'}), 404
