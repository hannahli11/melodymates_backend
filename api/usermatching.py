from flask import Blueprint, jsonify
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
class UsermatchingAPI:
    @staticmethod
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
# Match resources for each user
class HannahMatchResource(Resource):
    def get(self):
        match = UsermatchingAPI.find_music_match("Hannah")
        if match:
            return jsonify({"message": "Match found!", "match": match})
        return {"message": "No suitable match found"}, 404
class RheaMatchResource(Resource):
    def get(self):
        match = UsermatchingAPI.find_music_match("Rhea")
        if match:
            return jsonify({"message": "Match found!", "match": match})
        return {"message": "No suitable match found"}, 404
class CarsonMatchResource(Resource):
    def get(self):
        match = UsermatchingAPI.find_music_match("Carson")
        if match:
            return jsonify({"message": "Match found!", "match": match})
        return {"message": "No suitable match found"}, 404
class RowanMatchResource(Resource):
    def get(self):
        match = UsermatchingAPI.find_music_match("Rowan")
        if match:
            return jsonify({"message": "Match found!", "match": match})
        return {
            "message": "No suitable match found"}, 404
# Adding match resources to the API
api.add_resource(HannahMatchResource, '/match/Hannah')  # /api/match/Hannah
api.add_resource(RheaMatchResource, '/match/Rhea')      # /api/match/Rhea
api.add_resource(CarsonMatchResource, '/match/Carson')  # /api/match/Carson
api.add_resource(RowanMatchResource, '/match/Rowan')    # /api/match/Rowan