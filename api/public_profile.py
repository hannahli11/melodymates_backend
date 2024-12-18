from flask import Blueprint, jsonify, Flask
from flask_restful import Api, Resource # used for REST API building
from flask_cors import CORS 

profile_api = Blueprint('profile_api', __name__, url_prefix='/api')
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  
# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(profile_api)


class ProfileAPI:
   # @app.route('/api/student/')
    def get_user(name):
        users = {
            "Hannah": {
                "Name": "Hannah Li",
                "FavoriteArtists": "Gracie Abrams, Don Toliver, Ariana Grande",
                "Bio": "Music enthusiast and aspiring songwriter.",
                "ProfilePicture": "https://example.com/hannah_profile.jpg",
            },
            "Rhea": {
                "Name": "Rhea Rajashekar",
                "FavoriteArtists": "The Weeknd, Don Toliver, Metro Boomin",
                "Bio": "Music enthusiast and aspiring songwriter.",
                "ProfilePicture": "https://example.com/rhea_profile.jpg",
            },
            "Gaheera": {
                "Name": "Gaheera Babbar",
                "FavoriteArtists": "The Weeknd, Don Toliver, Ariana Grande",
                "Bio": "DNHS San Diego California.",
                "ProfilePicture": "https://example.com/gaheera_profile.jpg",
            },
            "Carson": {
                "Name": "Carson Sutherland",
                "FavoriteArtists": "Brent Faiyaz, Radiohead, Drake",
                "Bio": "Music enthusiast and aspiring songwriter.",
                "ProfilePicture": "https://example.com/carson_profile.jpg",
            },
            "Rowan": {
                "Name": "Rowan Sutherland",
                "FavoriteArtists": "Hozier,  Imogen Heap, Big Theif",
                "Bio": "Music enthusiast and aspiring songwriter.",
                "ProfilePicture": "https://example.com/rowan_profile.jpg",
            },
            "Brandon": {
                "Name": "Brandon Smurlo",
                "FavoriteArtists": "T-dre, Bryson Tiller, Bob Marley",
                "Bio": "Music enthusiast and aspiring songwriter.",
                "ProfilePicture": "https://example.com/brandon_profile.jpg",
            }
        }
        return users[name]
    
class HannahResource(Resource): 
    def get(self):
        user = ProfileAPI.get_user("Hannah")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
    
class RheaResource(Resource): 
     def get(self):
        user = ProfileAPI.get_user("Rhea")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
    
class RowanResource(Resource): 
      def get(self):
        user = ProfileAPI.get_user("Rowan")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
    
class GaheeraResource(Resource): 
      def get(self):
        user = ProfileAPI.get_user("Gaheera")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
class BrandonResource(Resource): 
      def get(self):
        user = ProfileAPI.get_user("Brandon")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
    
class CarsonResource(Resource): 
      def get(self):
        user = ProfileAPI.get_user("Carson")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
      
# Building REST API endpoint
api.add_resource(HannahResource, '/profile/Hannah')
api.add_resource(RheaResource, '/profile/Rhea')
api.add_resource(GaheeraResource, '/profile/Gaheera')
api.add_resource(RowanResource, '/profile/Rowan')
api.add_resource(CarsonResource, '/profile/Carson')
api.add_resource(BrandonResource, '/profile/Brandon')
