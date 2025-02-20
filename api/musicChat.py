from flask import Flask, Blueprint, jsonify, request
from flask_restful import Api
from flask_cors import CORS
from __init__ import app, db
from model.musicChat import MusicChat
from model.user import User  # Ensure User model is imported

# Initialize Blueprint for MusicChat API
musicChat_api = Blueprint('musicChat_api', __name__, url_prefix='/api/music_chat')
CORS(musicChat_api, supports_credentials=True, origins='*')

api = Api(musicChat_api)

# Helper function to censor inappropriate words
def censor_message(text):
    banned_words = ["inappropriate"]
    words = text.split()
    return " ".join(["***" if word.lower() in banned_words else word for word in words])

# Ensure database is initialized
@app.before_request
def initialize_database():
    with app.app_context():
        db.create_all()

# 📌 POST: Send a message
@musicChat_api.route('/chat', methods=['POST'])
def send_message():
    try:
        data = request.json
        if not data or "message" not in data or "user_id" not in data:
            return jsonify({"error": "Invalid input"}), 400

        message = data["message"]
        user_id = data["user_id"]

        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User ID does not exist"}), 400

        censored_msg = censor_message(message)

        # Create and save chat message
        chat = MusicChat(message=censored_msg, user_id=user_id)
        db.session.add(chat)
        db.session.commit()

        return jsonify({
            "message": "Message sent successfully",
            "original_message": message,
            "censored_message": censored_msg,
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# 📌 GET: Fetch all chat history
@musicChat_api.route('/chat', methods=['GET'])
def get_all_chats():
    try:
        chats = MusicChat.query.all()
        return jsonify([chat.read() for chat in chats]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 📌 GET: Fetch a specific chat by ID
@musicChat_api.route('/chat/<int:chat_id>', methods=['GET'])
def get_chat(chat_id):
    try:
        chat = MusicChat.query.get(chat_id)
        if not chat:
            return jsonify({"message": "Chat not found"}), 404
        return jsonify(chat.read()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 📌 PUT: Edit (update) a message
@musicChat_api.route('/chat/<int:chat_id>', methods=['PUT'])
def edit_message(chat_id):
    try:
        data = request.json
        if not data or "message" not in data:
            return jsonify({"error": "Invalid input"}), 400

        chat = MusicChat.query.get(chat_id)
        if not chat:
            return jsonify({"message": "Chat not found"}), 404

        chat._message = censor_message(data["message"])
        db.session.commit()

        return jsonify({"message": "Message updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# 📌 DELETE: Delete a message
@musicChat_api.route('/chat/<int:chat_id>', methods=['DELETE'])
def delete_message(chat_id):
    try:
        chat = MusicChat.query.get(chat_id)
        if not chat:
            return jsonify({"message": "Chat not found"}), 404

        db.session.delete(chat)
        db.session.commit()

        return jsonify({"message": "Message deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# 📌 GET: Get chat history between two users
@musicChat_api.route('/chat_history/<int:user1>/<int:user2>', methods=['GET'])
def get_chat_history(user1, user2):
    try:
        chat_history = MusicChat.query.filter(
            (MusicChat._user_id == user1) | (MusicChat._user_id == user2)
        ).all()

        if not chat_history:
            return jsonify({"message": "No chat history found"}), 404

        return jsonify([chat.read() for chat in chat_history]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Register Blueprint with the Flask app
# app.register_blueprint(musicChat_api)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8404)
