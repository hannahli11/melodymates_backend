from flask import Blueprint, jsonify, Flask
from flask_restful import Api, Resource
from flask_cors import CORS  # Handles cross-origin requests
from model.musicpref import MusicPref

# Set up the Flask app and API
usermatching_api = Blueprint('usermatching_api', __name__, url_prefix='/api')  # Blueprint for modular API
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allows frontend to talk to the backend without issues
api = Api(usermatching_api)  # Connect the API to the Blueprint

# This is where we store all the user info (static data)
class UserMatchingAPI:
    @staticmethod
    def get_user(name):
        users = {
            "Hannah": {
                "preferences": {
                    "Black Star - Radiohead": "No",
                    "Sicko Mode - Travis Scott": "Yes",
                    "Bad Guy - Billie Eilish": "No",
                    "No Tears Left to Cry - Ariana Grande": "Yes",
                    "Ex-Factor - Lauryn Hill": "No"
                },
                "bio": "Hannah loves pop music and high-energy beats."
            },
            "Rhea": {
                "preferences": {
                    "Black Star - Radiohead": "Yes",
                    "Sicko Mode - Travis Scott": "No",
                    "Bad Guy - Billie Eilish": "Yes",
                    "No Tears Left to Cry - Ariana Grande": "No",
                    "Ex-Factor - Lauryn Hill": "Yes"
                },
                "bio": "Rhea enjoys soulful tunes and lyrical depth."
            },
            "Carson": {
                "preferences": {
                    "Black Star - Radiohead": "No",
                    "Sicko Mode - Travis Scott": "Yes",
                    "Bad Guy - Billie Eilish": "No",
                    "No Tears Left to Cry - Ariana Grande": "Yes",
                    "Ex-Factor - Lauryn Hill": "No"
                },
                "bio": "Carson is into upbeat tracks and modern hits."
            },
            "Rowan": {
                "preferences": {
                    "Black Star - Radiohead": "Yes",
                    "Sicko Mode - Travis Scott": "No",
                    "Bad Guy - Billie Eilish": "Yes",
                    "No Tears Left to Cry - Ariana Grande": "No",
                    "Ex-Factor - Lauryn Hill": "Yes"
                },
                "bio": "Rowan loves alternative and indie music."
            }
        }
        # Try to get the user data by name, or return None if not found
        return users.get(name)

# Each class below is basically an endpoint for one user's data
class HannahResource(Resource):
    def get(self):
        user = UserMatchingAPI.get_user("Hannah")
        if user:  # If we found the user, return their data
            return jsonify(user)
        return {"Data not found"}, 404  # If no data, send a 404 error

class RheaResource(Resource):
    def get(self):
        user = UserMatchingAPI.get_user("Rhea")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404

class CarsonResource(Resource):
    def get(self):
        user = UserMatchingAPI.get_user("Carson")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404

class RowanResource(Resource):
    def get(self):
        user = UserMatchingAPI.get_user("Rowan")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404

# Add routes for each user. The URL will map to the right resource.
api.add_resource(HannahResource, '/match/Hannah')  # /api/match/Hannah
api.add_resource(RheaResource, '/match/Rhea')      # /a"Ex-Factor - Lauryn Hill"pi/match/Rhea
api.add_resource(CarsonResource, '/match/Carson')  # /api/match/Carson
api.add_resource(RowanResource, '/match/Rowan')    # /api/match/Rowan

# Register the Blueprint with the Flask app
app.register_blueprint(usermatching_api)

if __name__ == "__main__":
    app.run(debug=True)
