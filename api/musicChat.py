from flask import Flask, Blueprint, jsonify, request
from flask_restful import Api
from flask_cors import CORS

# Initialize a Flask application
musicChat_api = Blueprint('musicChat_api', __name__, url_prefix='/api/music_chat')
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

api = Api(musicChat_api)

# Simulating in-memory active users and chats for the sake of example
active_users = []  # Users who are currently logged in
chats = {}  # Dictionary to store chats between users

# API endpoint to send a message
@musicChat_api.route('/chat', methods=['POST']) # endpoint to post a message on chatroom (POST METHOD)
def send_message(): # function to send messages is defined
    data = request.json
    if not data or "message" not in data or "user_id" not in data:
        return jsonify({"error": "Invalid input"}), 400

    message = data["message"]
    user_id = data["user_id"]

   
    chat_id = len(chats) + 1  
    chats[chat_id] = {"message": message, "user_id": user_id}

    return jsonify({"message": "Message sent successfully", "chat_id": chat_id}), 200


# API endpoint to get a chat message by ID
@musicChat_api.route('/chat/<int:chat_id>', methods=['GET'])
def get_chat(chat_id):
    chat = chats.get(chat_id)
    if not chat:
        return jsonify({"message": "Chat not found"}), 404

    return jsonify({"chat_id": chat_id, "message": chat["message"], "user_id": chat["user_id"]}), 200

# API endpoint to fetch all messages
@musicChat_api.route('/chat', methods=['GET'])
def get_all_chats():
    return jsonify(chats), 200

