from flask import request, jsonify, g
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from __init__ import db
from model.artInfo import ArtInfo  # Ensure your `ArtInfo` model is imported correctly

class ArtInfoCRUD(Resource):
    def post(self):
        """
        Create a new artist entry in the database.

        Returns:
            JSON response with the created artist details or an error message.
        """
        body = request.get_json()

        # Validate required fields
        name = body.get('name')
        uid = body.get('uid')
        favorites = body.get('favorites', [])

        if not name or len(name) < 2:
            return {'message': 'Name is missing or too short (minimum 2 characters).'}, 400
        if not uid or len(uid) < 2:
            return {'message': 'UID is missing or too short (minimum 2 characters).'}, 400

        # Create a new ArtInfo instance
        new_artist = ArtInfo(name=name, uid=uid, favorites=favorites)

        try:
            new_artist.create()
        except IntegrityError as e:
            db.session.rollback()
            return {'message': f'Error creating artist: {e}'}, 400

        return jsonify(new_artist.read())

    def get(self):
        """
        Retrieve all artist entries from the database.

        Returns:
            JSON response with a list of artist details.
        """
        artists = ArtInfo.query.all()
        return jsonify([artist.read() for artist in artists])

    def put(self):
        """
        Update an existing artist entry in the database.

        Returns:
            JSON response with the updated artist details or an error message.
        """
        body = request.get_json()
        uid = body.get('uid')

        if not uid:
            return {'message': 'UID is required to update artist details.'}, 400

        # Retrieve the artist by UID
        artist = ArtInfo.query.filter_by(_uid=uid).first()
        if not artist:
            return {'message': f'Artist with UID {uid} not found.'}, 404

        # Update the artist's details
        artist.update(body)
        return jsonify(artist.read())

    def delete(self):
        """
        Delete an artist entry from the database.

        Returns:
            JSON response with a success message or an error message.
        """
        body = request.get_json()
        uid = body.get('uid')

        if not uid:
            return {'message': 'UID is required to delete an artist.'}, 400

        # Retrieve the artist by UID
        artist = ArtInfo.query.filter_by(_uid=uid).first()
        if not artist:
            return {'message': f'Artist with UID {uid} not found.'}, 404

        # Delete the artist
        artist_json = artist.read()
        artist.delete()
        return f"Deleted artist: {artist_json}", 204
