from flask import Blueprint, jsonify, Flask
from flask_restful import Api, Resource # used for REST API building
from flask_cors import CORS 


information_api = Blueprint('information_api', __name__, url_prefix='/api')
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  
# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(information_api)

class InformationAPI:
   # @app.route('/api/information/')
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
      
# Building REST API endpoint
api.add_resource(HannahResource, '/data/Hannah')
api.add_resource(RheaResource, '/data/Rhea')
api.add_resource(GaheeraResource, '/data/Gaheera')
api.add_resource(RowanResource, '/data/Rowan')
api.add_resource(CarsonResource, '/data/Carson')
api.add_resource(BrandonResource, '/data/Brandon')
