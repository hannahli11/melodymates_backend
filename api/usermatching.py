from flask import Blueprint, jsonify
from flask_restful import Api, Resource  # used for REST API building
usermatching_api = Blueprint('usermatching_api', __name__, url_prefix='/api')
api = Api(usermatching_api)
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
    return users.get(name, None)

# Function to find the best music match
def find_music_match(username):
    current_user = users.get(username)
    if not current_user:
        return None

    best_match = None
    max_score = 0

    for user, data in users.items():
        if user == username:
            continue
        score = 0
        if data["FavoriteArtist"] == current_user["FavoriteArtist"]:
            score += 2
        if data["Era"] == current_user["Era"]:
            score += 2
        if data["FavoriteAspect"] == current_user["FavoriteAspect"]:
            score += 1
        if data["DiscoveryMethod"] == current_user["DiscoveryMethod"]:
            score += 1
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

# Registering API endpoints
for user in users.keys():
    api.add_resource(UserResource, f'/data/{user}', resource_class_kwargs={'username': user})

# Building REST API endpoint
api.add_resource(HannahResource, '/match/Hannah')
api.add_resource(RheaResource, '/match/Rhea')
api.add_resource(GaheeraResource, '/match/Gaheera')
api.add_resource(RowanResource, '/match/Rowan')
api.add_resource(CarsonResource, '/match/Carson')
api.add_resource(BrandonResource, '/match/Brandon')