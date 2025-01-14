from flask import Blueprint, jsonify
from flask_restful import Api, Resource

# Create a Flask Blueprint
usermatching_api = Blueprint('usermatching_api', __name__, url_prefix='/api')
api = Api(usermatching_api)

# Sample user music preferences database
music_preferences = {
    "Hannah": {
        "Black Star - Radiohead": "No",
        "Sicko Mode - Travis Scott": "Yes",
        "Bad Guy - Billie Eilish": "No",
        "No Tears Left to Cry - Ariana Grande": "Yes",
        "Ex-Factor - Lauryn Hill": "No"
    },
    "Rhea": {
        "Black Star - Radiohead": "Yes",
        "Sicko Mode - Travis Scott": "No",
        "Bad Guy - Billie Eilish": "Yes",
        "No Tears Left to Cry - Ariana Grande": "No",
        "Ex-Factor - Lauryn Hill": "Yes"
    },
    "Carson": {
        "Black Star - Radiohead": "No",
        "Sicko Mode - Travis Scott": "Yes",
        "Bad Guy - Billie Eilish": "No",
        "No Tears Left to Cry - Ariana Grande": "Yes",
        "Ex-Factor - Lauryn Hill": "No"
    },
    "Rowan": {
        "Black Star - Radiohead": "Yes",
        "Sicko Mode - Travis Scott": "No",
        "Bad Guy - Billie Eilish": "Yes",
        "No Tears Left to Cry - Ariana Grande": "No",
        "Ex-Factor - Lauryn Hill": "Yes"
    }
}

# Function to retrieve a user's music preferences
def get_user_preferences(name):
    return music_preferences.get(name, None)

# Function to find the best music match
def find_music_match(username):
    current_user = music_preferences.get(username)
    if not current_user:
        return None

    best_match = None
    max_score = 0

    for user, data in music_preferences.items():
        if user == username:
            continue
        score = sum(1 for song in current_user if current_user[song] == data.get(song, None))

        if score > max_score:
            max_score = score
            best_match = {"username": user, **data}

    return best_match

# Individual user data endpoints
class UserResource(Resource):
    def get(self, username):
        user = get_user_preferences(username)
        if user:
            return jsonify(user)
        return {"message": "User not found"}, 404

# Matchmaking endpoint
class MatchResource(Resource):
    def get(self, username):
        match = find_music_match(username)
        if match:
            return jsonify({"message": "Match found!", "match": match})
        return {"message": "No suitable match found"}, 404

# Register API endpoints dynamically
api.add_resource(UserResource, '/data/<string:username>')
api.add_resource(MatchResource, '/match/<string:username>')
