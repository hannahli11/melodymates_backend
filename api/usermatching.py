from flask import Blueprint, jsonify, Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS


# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Enable CORS for all origins


# Define the Blueprint for the API
profilematching_api = Blueprint('profilematching_api', __name__, url_prefix='/api')
api = Api(profilematching_api)


app.register_blueprint(profilematching_api)


# Sample user data
class ProfilematchingAPI:
    def get_user(self, name):
        users = {
            "Alex": {
                "Username": "alex_rocker",
                "FavoriteArtists": "Radiohead",
                "ArtistRecommendation": "Pink Floyd, Nirvana",
                "TopSong": "Black Star",
                "ListeningTime": "4:07"
            },
            "Rhea": {
                "Username": "rhear_02",
                "FavoriteArtists": "The Weeknd, Don Toliver, Metro Boomin",
                "ArtistRecommendation": "Drake, Lil Uzi Vert, 21 Savage",
                "TopSong": "Save Your Tears",
                "ListeningTime": "3:50"
            },
            "Gaheera": {
                "Username": "gaheerb",
                "FavoriteArtists": "Future, Don Toliver, Travis Scott",
                "ArtistRecommendation": "Roddy Rich, NAV, PartyNextDoor",
                "TopSong": "Mask Off",
                "ListeningTime": "4:30"
            }
            # Add other users here
        }
        return users.get(name)


# Resource for user profiles
class UserProfileResource(Resource):
    def get(self, name):
        user = ProfilematchingAPI().get_user(name)
        if user:
            return jsonify(user)
        return {"message": "User not found"}, 404


# Resource for handling decisions (approved/rejected)
class UserDecisionResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        decision = data.get('decision')


        # Process decision (for simplicity, just print it here)
        if username and decision:
            # Here you could save the decision to a database or perform other actions
            return {"message": "Decision for {username} is {decision}"}, 200
        return {"message": "Invalid data"}, 400


# Add resources to the API
api.add_resource(UserProfileResource, '/user/<string:name>')
api.add_resource(UserDecisionResource, '/user-status')


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)


