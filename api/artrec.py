from flask import Blueprint, jsonify, Flask, request
from flask_restful import Api, Resource # used for REST API building
# from flask_cors import CORS

from model.artInfo import ArtInfo 

artrec_api = Blueprint('artrec_api', __name__, url_prefix='/api') 
app = Flask(__name__)
# CORS(app, supports_credentials=True, origins='*')
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
        # Ensure favorites is a list, even if it's a single artist
        if isinstance(favorites, str):
            favorites = [favorites]  # Convert single artist to a list
        elif not isinstance(favorites, list):
            return {'message': 'Favorites must be a list of artist names or a single artist name'}, 400


        # Setup ArtInfo object
        artist = ArtInfo(name=name, uid=uid, favorites=favorites)

        artist.create()
        if not artist:  # failure returns error message
                return {'message': f'Processed {name}'}, 400
        return jsonify(artist.read())

    def get_recommended_artists(self, favorites):
        # Sample recommendations based on favorite artists
        recommendations = {
            "Gracie Abrams": ["Olivia Rodrigo", "Chloe Moriondo", "Maisie Peters"],
            "Don Toliver": ["Travis Scott", "Lil Uzi Vert", "Kid Cudi"],
            "Ariana Grande": ["Demi Lovato", "Beyoncé", "Rihanna"],
            "The Weeknd": ["Drake", "Post Malone", "Travis Scott"],
            "Bob Marley": ["Peter Tosh", "Jimmy Cliff", "Burning Spear"]            # Add more mappings as necessary
        }
        
        # Start with an empty list for recommendations
        recommended_artists = []
        
        # Loop through each favorite artist and fetch recommendations
        for artist in favorites:
            if artist in recommendations:
                recommended_artists.extend(recommendations[artist])
        
        # Remove duplicates and return the list
        return list(set(recommended_artists))[:5]  # Limit to 5 artists

    
    def get(self):
        # Check if a UID query parameter is provided
        uid = request.args.get('uid')
        if uid:
            artist = ArtInfo.query.filter_by(_uid=uid).first()
            if not artist:
                return {'message': f'Artist with UID {uid} not found'}, 404
            
            # Fetch recommended artists based on their favorite artists
            recommended_artists = self.get_recommended_artists(artist.favorites)
            artist_data = artist.read()
            artist_data['recommended_artists'] = recommended_artists  # Add the recommendations
            
            return jsonify(artist_data)
        else:
            artists = ArtInfo.query.all()
            if not artists:
                return {'message': 'No artist records found'}, 404
            json_ready = []
            for artist in artists:
                recommended_artists = self.get_recommended_artists(artist.favorites)
                artist_data = artist.read()
                artist_data['recommended_artists'] = recommended_artists
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
        
        # Bad request: artist not foun
        if artist is None:
            return {'message': f'ArtInfo record with UID {uid} not found'}, 404
        
        # Read and then delete the ArtInfo record using custom methods
        artist_json = artist.read()
        artist.delete()
        
        # 204 is the status code for delete with no JSON response
        return f"Deleted ArtInfo record: {artist_json}", 204  # Use 200 to test with Postman




      
# Building REST API endpoint
api.add_resource(ArtInfoResource, '/artinfo') # POST, GET, PUT, DELETE for /api/artinfo
api.add_resource(HannahResource, '/user/Hannah')
api.add_resource(RheaResource, '/user/Rhea')
api.add_resource(GaheeraResource, '/user/Gaheera')
api.add_resource(RowanResource, '/user/Rowan')
api.add_resource(CarsonResource, '/user/Carson')
api.add_resource(BrandonResource, '/user/Brandon')




