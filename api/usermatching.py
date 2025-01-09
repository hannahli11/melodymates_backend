import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.post import Post
from model.channel import Channel
usermatching_api = Blueprint('usermatching_api', __name__, url_prefix='/api')
api = Api(usermatching_api)

# Sample user music preferences database
users = {
    "Hannah": {
        "FavoriteArtist": "Taylor Swift",
        "MusicPlatform": "Spotify",
        "DiscoveryMethod": "Friends/Family",
        "ListeningFrequency": "Several times a week",
        "Era": "1980's",
        "FavoriteAspect": "Vocals"
    },
    "Rhea": {
        "FavoriteArtist": "SZA",
        "MusicPlatform": "Spotify",
        "DiscoveryMethod": "Social Media",
        "ListeningFrequency": "Several times a week",
        "Era": "2010's",
        "FavoriteAspect": "Beat"
    },
    "Carson": {
        "FavoriteArtist": "Frank Ocean",
        "MusicPlatform": "Spotify",
        "DiscoveryMethod": "Social Media",
        "ListeningFrequency": "Everyday",
        "Era": "Modern",
        "FavoriteAspect": "Rhythm"
    },
    "Rowan": {
        "FavoriteArtist": "Taylor Swift",
        "MusicPlatform": "Spotify",
        "DiscoveryMethod": "Music blogs",
        "ListeningFrequency": "Everyday",
        "Era": "1990's",
        "FavoriteAspect": "Vocals"
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

api.add_resource(MatchResource, '/match/<string:username>')
