from flask import Blueprint, jsonify
from flask_restful import Api, Resource # used for REST API building
information_api = Blueprint('information_api', __name__, url_prefix='/api')
# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(information_api) # Connect the API to the Blueprint

#Static data for group members stored here
class InformationAPI:
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
        return users[name]
    # Try to get the student data by name, or return None if not found return "Data not found"
class HannahResource(Resource):
    def get(self):
        user = InformationAPI.get_user("Hannah")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
class RheaResource(Resource):
     def get(self):
        user = InformationAPI.get_user("Rhea")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
class RowanResource(Resource):
      def get(self):
        user = InformationAPI.get_user("Rowan")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
class GaheeraResource(Resource):
      def get(self):
        user = InformationAPI.get_user("Gaheera")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
class BrandonResource(Resource):
      def get(self):
        user = InformationAPI.get_user("Brandon")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
class CarsonResource(Resource):
      def get(self):
        user = InformationAPI.get_user("Carson")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
# Add routes for each student. The URL will map to the right resource.
api.add_resource(HannahResource, '/data/Hannah')
api.add_resource(RheaResource, '/data/Rhea')
api.add_resource(GaheeraResource, '/data/Gaheera')
api.add_resource(RowanResource, '/data/Rowan')
api.add_resource(CarsonResource, '/data/Carson')
api.add_resource(BrandonResource, '/data/Brandon')