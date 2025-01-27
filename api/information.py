from flask import Blueprint, jsonify, Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from model.musicpref import MusicPref  # Importing your MusicPref model
from __init__ import db  # Import the db object from __init__.py

# Set up the Flask app and API
information_api = Blueprint('information_api', __name__, url_prefix='/api')
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allows frontend to talk to the backend without issues
api = Api(information_api)  # Connect the API to the Blueprint

# Class for handling MusicPref data input and storing in the database
class MusicPrefResource(Resource):
    def post(self):
        """
        Create a new MusicPref record.
        """
        data = request.get_json()  # Get JSON data from the request
        if not data:
            return {'message': 'No input data provided'}, 400

        # Extracting the necessary fields from the incoming data
        name = data.get('name')
        uid = data.get('uid')
        favorites = data.get('favorites', [])
        music_platform = data.get('music_platform')
        learn_preference = data.get('learn_preference')
        listening_frequency = data.get('listening_frequency')
        favorite_era = data.get('favorite_era')
        important_aspect = data.get('important_aspect')

        # Create a new MusicPref object using the provided data
        user = MusicPref(name=name, uid=uid, favorites=favorites, music_platform=music_platform, 
                         learn_preference=learn_preference, listening_frequency=listening_frequency, 
                         favorite_era=favorite_era, important_aspect=important_aspect)

        # Save the new user data to the database
        user.create()

        # Return the stored user data as a JSON response
        return jsonify(user.read())

    def put(self):
        """
        Update an existing MusicPref record in the database.

        Retrieves the record by 'uid' and updates it based on the JSON body of the request.
        """
        body = request.get_json()  # Read data from the JSON body of the request
        uid = body.get('uid')  # Get the unique identifier

        # Ensure the UID is provided
        if not uid:
            return {'message': 'UID is required to update a record'}, 400

        # Find the user record by UID
        user = MusicPref.query.filter_by(uid=uid).first()
        if user is None:
            return {'message': f'MusicPref record with UID {uid} not found'}, 404

        # Update the fields if provided in the body
        if 'name' in body:
            user.name = body['name']
        if 'favorites' in body:
            user.favorites = body['favorites']
        if 'music_platform' in body:
            user.music_platform = body['music_platform']
        if 'learn_preference' in body:
            user.learn_preference = body['learn_preference']
        if 'listening_frequency' in body:
            user.listening_frequency = body['listening_frequency']
        if 'favorite_era' in body:
            user.favorite_era = body['favorite_era']
        if 'important_aspect' in body:
            user.important_aspect = body['important_aspect']

        # Commit the changes to the database
        db.session.commit()

        # Return the updated record as a JSON response
        return jsonify(user.read())

    def delete(self):
        """
        Delete a MusicPref record by 'uid'.
        """
        body = request.get_json()  # Read data from the JSON body of the request
        uid = body.get('uid')  # Get the unique identifier

        # Ensure the UID is provided
        if not uid:
            return {'message': 'UID is required to delete a record'}, 400

        # Find the user record by UID
        user = MusicPref.query.filter_by(uid=uid).first()
        if user is None:
            return {'message': f'MusicPref record with UID {uid} not found'}, 404

        # Delete the user record
        db.session.delete(user)
        db.session.commit()

        # Return a success message
        return {'message': f'MusicPref record with UID {uid} deleted successfully'}, 200


# Class for handling retrieval of all MusicPref records
class MusicPrefInfoResource(Resource):
    def get(self):
        """
        Retrieves all MusicPref records from the database.
        """
        users = MusicPref.query.all()  # Fetch all records
        json_ready = [user.read() for user in users]  # Prepare a list of dictionaries
        return jsonify(json_ready)


# Add the resource to the API
api.add_resource(MusicPrefResource, '/data/musicpref')  # (POST/PUT/DELETE) /api/data/musicpref
api.add_resource(MusicPrefInfoResource, '/data/musicpref/all')  # (GET) /api/data/musicpref/all

# Register the Blueprint with the Flask app
app.register_blueprint(information_api)

if __name__ == "__main__":
    app.run(debug=True)
