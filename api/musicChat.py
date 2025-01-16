from flask import Flask, Blueprint, jsonify, request
from flask_restful import Api
from flask_cors import CORS
from __init__ import app, db
from model.musicChat import MusicChat  

# Initialize a Blueprint for the music chat API
musicChat_api = Blueprint('musicChat_api', __name__, url_prefix='/api/music_chat')
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

api = Api(musicChat_api)

# API endpoint to send a message
@musicChat_api.route('/chat', methods=['POST'])
def send_message():
    try:
        data = request.json
        if not data or "message" not in data or "user_id" not in data:
            return jsonify({"error": "Invalid input"}), 400

        # Extract data
        message = data["message"]
        user_id = data["user_id"]

        # Create a new MusicChat object and save to database
        chat = MusicChat(message=message, user_id=user_id)
        chat.create()

        return jsonify({"message": "Message sent successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint to fetch all chat history
@musicChat_api.route('/chat', methods=['GET'])
def get_all_chats():
    try:
        # Fetch all chat records from the database
        chats = MusicChat.query.all()
        return jsonify([chat.read() for chat in chats]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint to fetch a specific chat by ID
@musicChat_api.route('/chat/<int:chat_id>', methods=['GET'])
def get_chat(chat_id):
    try:
        # Fetch the specific chat record by ID
        chat = MusicChat.query.get(chat_id)
        if not chat:
            return jsonify({"message": "Chat not found"}), 404

        return jsonify(chat.read()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint to fetch chat history between two users
@musicChat_api.route('/chat_history/<int:user1>/<int:user2>', methods=['GET'])
def get_chat_history(user1, user2):
    try:
        # Fetch chat history between the two users
        chat_history = MusicChat.query.filter(
            (MusicChat._user_id == user1) | (MusicChat._user_id == user2)
        ).all()

        if not chat_history:
            return jsonify({"message": "No chat history found"}), 404

        return jsonify([chat.read() for chat in chat_history]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Register the Blueprint
# app.register_blueprint(musicChat_api)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8887")
