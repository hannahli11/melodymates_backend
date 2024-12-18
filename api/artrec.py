from flask import Blueprint, jsonify, Flask
from flask_restful import Api, Resource # used for REST API building
from flask_cors import CORS 

artrec_api = Blueprint('artrec_api', __name__, url_prefix='/api')
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  
# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(artrec_api)


class ArtrecAPI:
   # @app.route('/api/student/')
    def get_user(name):
        users = {
            "Hannah": {
                "Username": "hannahli_11",
                "FavoriteArtists": "Gracie Abrams, Don Toliver, Ariana Grande",
                "ArtistReccomendation": "Travis Scott, SZA, Phoebe Bridgers"
            },
            "Rhea": {
                "Username": "rhear_02",
                "FavoriteArtists": "The Weeknd, Don Toliver, Metro Boomin",
                "ArtistReccomendation": "Drake, Lil Uzi Vert, 21 Savage"
            },
            "Gaheera": {
                "Username": "gaheerb",
                "FavoriteArtists": "Future, Don Toliver, Travis Scott",
                "ArtistReccomendation": "Roddy Rich, NAV, PartyNextDoor"
            },
            "Carson": {
                "Username": "carsonsuth17",
                "FavoriteArtists": "Brent Faiyaz, Radiohead, Drake",
                "ArtistReccomendation": "Giveon, Tame Impala, J. Cole"
            },
            "Rowan": {
                "Username": "rowangs",
                "FavoriteArtists": "Hozier,  Imogen Heap, Big Theif",
                "ArtistReccomendation": "Leon Bridges, Grimes, Phoebe Bridgers"
            },
             "Brandon": {
                "Username": "bsmurlo",
                "FavoriteArtists": "T-dre, Bryson Tiller, Bob Marley",
                "ArtistReccomendation": "J. Cole, Torey Lanez, Peter Tosh"
            }
        }
        return users[name]
    
class HannahResource(Resource): 
    def get(self):
        user = ArtrecAPI.get_user("Hannah")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
    
class RheaResource(Resource): 
     def get(self):
        user = ArtrecAPI.get_user("Rhea")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
    
class RowanResource(Resource): 
      def get(self):
        user = ArtrecAPI.get_user("Rowan")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
    
class GaheeraResource(Resource): 
      def get(self):
        user = ArtrecAPI.get_user("Gaheera")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
class BrandonResource(Resource): 
      def get(self):
        user = ArtrecAPI.get_user("Brandon")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
    
class CarsonResource(Resource): 
      def get(self):
        user = ArtrecAPI.get_user("Carson")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
      
# Building REST API endpoint
api.add_resource(HannahResource, '/user/Hannah')
api.add_resource(RheaResource, '/user/Rhea')
api.add_resource(GaheeraResource, '/user/Gaheera')
api.add_resource(RowanResource, '/user/Rowan')
api.add_resource(CarsonResource, '/user/Carson')
api.add_resource(BrandonResource, '/user/Brandon')
