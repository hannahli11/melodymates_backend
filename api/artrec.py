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
      
class ArtInfoResource(Resource):
    def post(self):  # Debug log
        body = request.get_json()
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
        artist = ArtInfo(name=name, uid=uid, favorites=favorites)

        artist.create()
        if not artist:  # failure returns error message
                return {'message': f'Processed {name}'}, 400
        return jsonify(artist.read())


    def get(self):
        """
        Retrieves all artist records from the database.
        """
        artists = ArtInfo.query.all()  # Fetch all records

        # Prepare a list of dictionaries
        json_ready = []
        for artist in artists:
            artist_data = artist.read()
            json_ready.append(artist_data)

        return jsonify(json_ready)  
    
    def put(self):
        """
        Update artist details.

        Retrieves the current artist based on the passed UID (from request body or query parameters)
        and updates the artist details.

        Returns:
            JSON response with the updated artist details or an error message.
        """
        # Read data from the JSON body of the request
        body = request.get_json()

        # Ensure we have data in the body
        if not body:
            return {'message': 'No data provided'}, 400

        # Get the artist's UID from the request body or query params
        uid = body.get('uid') or request.args.get('uid')
        if not uid:
            return {'message': 'UID is required to update artist details'}, 400

        # Find the artist by UID
        artist = ArtInfo.query.filter_by(_uid=uid).first()
        if artist is None:
            return {'message': f'Artist with UID {uid} not found'}, 404

        # Perform the update logic
        try:
            artist.update(body)  # Assuming the update method exists on the artist object
        except Exception as e:
            return {'message': f'Error updating artist: {str(e)}'}, 500

        # Return response with updated artist details
        return jsonify(artist.read())
    
    def delete(self):
        """
        Delete an ArtInfo record.

        Deletes an ArtInfo record from the database based on the JSON body of the request.

        Returns:
            JSON response with a success message or an error message.
        """
        body = request.get_json()
        uid = body.get('uid')
        
        """ ArtInfo SQLAlchemy query returning a single record """
        artist = ArtInfo.query.filter_by(_uid=uid).first()
        
        # Bad request: artist not found
        if artist is None:
            return {'message': f'ArtInfo record with UID {uid} not found'}, 404
        
        # Read and then delete the ArtInfo record using custom methods
        artist_json = artist.read()
        artist.delete()
        
        # 204 is the status code for delete with no JSON response
        return f"Deleted ArtInfo record: {artist_json}", 204  # Use 200 to test with Postman




      
# Building REST API endpoint
api.add_resource(HannahResource, '/user/Hannah')
api.add_resource(RheaResource, '/user/Rhea')
api.add_resource(GaheeraResource, '/user/Gaheera')
api.add_resource(RowanResource, '/user/Rowan')
api.add_resource(CarsonResource, '/user/Carson')
api.add_resource(BrandonResource, '/user/Brandon')
api.add_resource(ArtInfoResource, '/artinfo')  # POST, GET, PUT, DELETE for /api/artinfo



