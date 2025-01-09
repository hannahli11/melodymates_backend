from flask import Blueprint, jsonify, Flask
from flask_restful import Api, Resource
from flask_cors import CORS  # Handles cross-origin requests

# Set up the Flask app and API
information_api = Blueprint('information_api', __name__, url_prefix='/api')  # Blueprint for modular API
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allows frontend to talk to the backend without issues
api = Api(information_api)  # Connect the API to the Blueprint

# This is where we store all the user info (static data)
class InformationAPI:
    @staticmethod
    def get_user(name):
        users = {
            "Hannah": {
                "ArtistPref": "Taylor Swift",
                "Method": "Spotify",
                "NewMusic": "Friends/Family",
                "HowOften": "Several times a week",
                "Era": "1980's",
                "FavoriteAspect": "Vocals"
            },
            "Rhea": {
                "ArtistPref": "SZA",
                "Method": "Spotify",
                "NewMusic": "Social Media",
                "HowOften": "Several times a week",
                "Era": "2010's",
                "FavoriteAspect": "Beat"
            },
            "Gaheera": {
                "ArtistPref": "Taylor Swift",
                "Method": "Spotify",
                "NewMusic": "Radio",
                "HowOften": "Every day",
                "Era": "2000's",
                "FavoriteAspect": "Vocals"
            },
            "Carson": {
                "ArtistPref": "Frank Ocean",
                "Method": "Spotify",
                "NewMusic": "Social Media",
                "HowOften": "Everyday",
                "Era": "Modern",
                "FavoriteAspect": "Rhythm"
            },
            "Rowan": {
                "ArtistPref": "Taylor Swift",
                "Method": "Spotify",
                "NewMusic": "Music blogs",
                "HowOften": "Everyday",
                "Era": "1990's",
                "FavoriteAspect": "Vocals"
            },
            "Brandon": {
                "ArtistPref": "Travis Scott",
                "Method": "Spotify",
                "NewMusic": "Social media",
                "HowOften": "Several times a week",
                "Era": "2000's",
                "FavoriteAspect": "Beat"
            }
        }
        # Try to get the user data by name, or return None if not found
        return users.get(name)

# Each class below is basically an endpoint for one user's data
class HannahResource(Resource):
    def get(self):
        user = InformationAPI.get_user("Hannah")
        if user:  # If we found the user, return their data
            return jsonify(user)
        return {"Data not found"}, 404  # If no data, send a 404 error

class RheaResource(Resource):
    def get(self):
        user = InformationAPI.get_user("Rhea")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404

class GaheeraResource(Resource):
    def get(self):
        user = InformationAPI.get_user("Gaheera")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404

class CarsonResource(Resource):
    def get(self):
        user = InformationAPI.get_user("Carson")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404

class RowanResource(Resource):
    def get(self):
        user = InformationAPI.get_user("Rowan")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404

class BrandonResource(Resource):
    def get(self):
        user = InformationAPI.get_user("Brandon")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404

# Add routes for each user. The URL will map to the right resource.
api.add_resource(HannahResource, '/data/Hannah')  # /api/data/Hannah
api.add_resource(RheaResource, '/data/Rhea')      # /api/data/Rhea
api.add_resource(GaheeraResource, '/data/Gaheera')  # /api/data/Gaheera
api.add_resource(CarsonResource, '/data/Carson')  # /api/data/Carson
api.add_resource(RowanResource, '/data/Rowan')    # /api/data/Rowan
api.add_resource(BrandonResource, '/data/Brandon')  # /api/data/Brandon

# Register the Blueprint with the Flask app
app.register_blueprint(information_api)

if __name__ == "__main__":
    app.run(debug=True)
