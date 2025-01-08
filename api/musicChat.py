from flask import Flask, Blueprint, jsonify, request
from flask_restful import Api, Resource
from model.musicChat import MusicChat  # Import your MusicChat model
from __init__ import app, db

# Initialize Flask blueprint
musicChat_api = Blueprint('musicChat_api', __name__, url_prefix='/api/music_chat')
api = Api(musicChat_api)

class MusicChatResource(Resource):
    def get(self, chat_id):
        """
        Fetch a specific music chat message by ID.
        """
        chat = MusicChat.query.get(chat_id)
        if chat:
            return jsonify(chat.read())
        return jsonify({"message": "Chat not found"}), 404

    def post(self):
        """
        Create a new music chat message.
        """
        data = request.json
        if not data or "message" not in data or "user_id" not in data:
            return jsonify({"error": "Invalid input"}), 400

        message = data["message"]
        user_id = data["user_id"]

        new_chat = MusicChat(message=message, user_id=user_id)
        try:
            new_chat.create()
            return jsonify({"message": "Chat message created successfully", "chat_id": new_chat.id}), 201
        except Exception as e:
            return jsonify({"error": f"Error occurred: {str(e)}"}), 500

# Add the resource to the API
api.add_resource(MusicChatResource, '/api/music_chat/chat', '/api/music_chat/chat/<int:chat_id>')
