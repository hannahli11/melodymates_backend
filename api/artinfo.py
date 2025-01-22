from flask import Blueprint, jsonify, Flask, request
from flask_restful import Api, Resource # used for REST API building
from flask_cors import CORS
from model.artInfo import ArtInfo 

artrec_api = Blueprint('artrec_api', __name__, url_prefix='/api')
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  
# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(artrec_api)


class ArtrecAPI:
    @staticmethod
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
      
class _addArtInfo(Resource):
    def post(self): 
        print("POST /artinfo/add called")  # Debug log
        body = request.get_json()
        print(f"Received body: {body}")

        # Validate name
        name = body.get('name')
        if name is None or len(name) < 2:
            return {'message': 'Name is missing, or is less than 2 characters'}, 400

        # Validate uid
        uid = body.get('uid')
        if uid is None or len(uid) < 2:
            return {'message': 'User ID is missing, or is less than 2 characters'}, 400

        # Validate favorites
        favorites = body.get('favorites', [])
        if not isinstance(favorites, list):
            return {'message': 'Favorites must be a list of artist names'}, 400

        # Setup ArtInfo object
        art_info_obj = ArtInfo(name=name, uid=uid, favorites=favorites)

        artist = art_info_obj.create()
        if not artist:  # failure returns error message
                return {'message': f'Processed {name}'}, 400
        return jsonify(artist.read())
    
      
# Building REST API endpoint
api.add_resource(HannahResource, '/user/Hannah')
api.add_resource(RheaResource, '/user/Rhea')
api.add_resource(GaheeraResource, '/user/Gaheera')
api.add_resource(RowanResource, '/user/Rowan')
api.add_resource(CarsonResource, '/user/Carson')
api.add_resource(BrandonResource, '/user/Brandon')
api.add_resource(_addArtInfo, '/artinfo/add')
app.register_blueprint(artrec_api)  # Register Blueprint with Flask app

if __name__ == "__main__":
    app.run(debug=True, port=8887) 

