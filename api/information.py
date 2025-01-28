from flask import Blueprint, jsonify, Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from model.musicpref import MusicPref  # Make sure this points to your model file

information_api = Blueprint('information_api', __name__, url_prefix='/api')
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')
api = Api(information_api)


class MusicPrefAPI:
    @staticmethod
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
        return users.get(name)


class HannahResource(Resource):
    def get(self):
        user = MusicPrefAPI.get_user("Hannah")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404


class RheaResource(Resource):
    def get(self):
        user = MusicPrefAPI.get_user("Rhea")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404


class RowanResource(Resource):
    def get(self):
        user = MusicPrefAPI.get_user("Rowan")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404


class GaheeraResource(Resource):
    def get(self):
        user = MusicPrefAPI.get_user("Gaheera")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404


class BrandonResource(Resource):
    def get(self):
        user = MusicPrefAPI.get_user("Brandon")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404


class CarsonResource(Resource):
    def get(self):
        user = MusicPrefAPI.get_user("Carson")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404


class MusicPrefResource(Resource):
    def post(self):
        body = request.get_json()

        name = body.get('name')
        if not name or len(name) < 2:
            return {'message': 'Name is missing, or is less than 2 characters'}, 400

        uid = body.get('uid')
        if not uid or len(uid) < 2:
            return {'message': 'User ID is missing, or is less than 2 characters'}, 400

        artist_pref = body.get('artist_pref')
        method = body.get('method')
        new_music = body.get('new_music')
        how_often = body.get('how_often')
        era = body.get('era')
        favorite_aspect = body.get('favorite_aspect')

        music_pref = MusicPref(
            name=name,
            uid=uid,
            favorites=[artist_pref],  # You can adjust this later if more artists are involved
            music_platform=method,
            learn_preference=new_music,
            listening_frequency=how_often,
            favorite_era=era,
            important_aspect=favorite_aspect
        )

        music_pref.create()
        return jsonify(music_pref.read())

    def get(self):
        music_prefs = MusicPref.query.all()
        json_ready = [music_pref.read() for music_pref in music_prefs]
        return jsonify(json_ready)

    def put(self):
        body = request.get_json()

        if not body:
            return {'message': 'No data provided'}, 400

        uid = body.get('uid') or request.args.get('uid')
        if not uid:
            return {'message': 'UID is required to update music preferences'}, 400

        music_pref = MusicPref.query.filter_by(_uid=uid).first()
        if music_pref is None:
            return {'message': f'Music preference with UID {uid} not found'}, 404

        music_pref.update(body)
        return jsonify(music_pref.read())

    def delete(self):
        body = request.get_json()
        uid = body.get('uid')

        music_pref = MusicPref.query.filter_by(_uid=uid).first()
        if music_pref is None:
            return {'message': f'Music preference with UID {uid} not found'}, 404

        music_pref.delete()
        return f"Deleted MusicPreference record: {music_pref.read()}", 204


api.add_resource(HannahResource, '/data/Hannah')
api.add_resource(RheaResource, '/data/Rhea')
api.add_resource(GaheeraResource, '/data/Gaheera')
api.add_resource(RowanResource, '/data/Rowan')
api.add_resource(CarsonResource, '/data/Carson')
api.add_resource(BrandonResource, '/data/Brandon')
api.add_resource(MusicPrefResource, '/musicpref')  # POST, GET, PUT, DELETE for /api/musicpref
