from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
import logging


usermatching_api = Blueprint('usermatching_api', __name__, url_prefix='/api')
api = Api(usermatching_api)

logging.basicConfig(level=logging.DEBUG)

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


def get_user_preferences(name):
    logging.debug(f"Fetching preferences for user: {name}")
    return music_preferences.get(name, None)


def find_music_match(username):
    logging.debug(f"Finding match for user: {username}")
    current_user = music_preferences.get(username)
    if not current_user:
        logging.debug(f"No preferences found for user: {username}")
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

    logging.debug(f"Best match for user {username}: {best_match}")
    return best_match


class UserResource(Resource):
    def get(self, username):
        logging.debug(f"GET request for user data: {username}")
        user = get_user_preferences(username)
        if user:
            return jsonify(user)
        logging.error(f"User not found: {username}")
        return {"message": "User not found"}, 404


class MatchResource(Resource):
    def get(self, username):
        logging.debug(f"GET request for match: {username}")
        match = find_music_match(username)
        if match:
            return jsonify({"message": "Match found!", "match": match})
        logging.error(f"No suitable match found for user: {username}")
        return {"message": "No suitable match found"}, 404


api.add_resource(UserResource, '/data/<string:username>')
api.add_resource(MatchResource, '/match/<string:username>')
