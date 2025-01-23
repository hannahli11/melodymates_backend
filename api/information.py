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

# Add the resource to the API
api.add_resource(MusicPrefResource, '/data/musicpref')  # /api/data/musicpref

# Register the Blueprint with the Flask app
app.register_blueprint(information_api)

if __name__ == "__main__":
    app.run(debug=True)
