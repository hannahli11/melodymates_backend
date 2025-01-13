from flask import Flask, Blueprint, jsonify, request
from flask_restful import Api
from flask_cors import CORS

# Initialize a Flask application and a Blueprint for the music chat API
musicChat_api = Blueprint('musicChat_api', __name__, url_prefix='/api/music_chat')
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

api = Api(musicChat_api)

# Hardcoded static data for chats and users
active_users = [
    {"user_id": 1, "username": "Alice"},
    {"user_id": 2, "username": "Bob"},
    {"user_id": 3, "username": "Charlie"}
]

chats = {
    1: {"message": "Hello, how are you?", "user_id": 1},
    2: {"message": "I'm good, thanks for asking!", "user_id": 2},
    3: {"message": "What's everyone listening to?", "user_id": 3}
}

# API endpoint to send a message
@musicChat_api.route('/chat', methods=['POST'])
def send_message():
    data = request.json
    if not data or "message" not in data or "user_id" not in data:
        return jsonify({"error": "Invalid input"}), 400

    message = data["message"]
    user_id = data["user_id"]

    chat_id = len(chats) + 1
    chats[chat_id] = {"message": message, "user_id": user_id}

    return jsonify({"message": "Message sent successfully"}), 200

# API endpoint to fetch all chat history
@musicChat_api.route('/chat', methods=['GET'])
def get_all_chats():
    return jsonify(chats), 200

# API endpoint to fetch specific chat by ID
@musicChat_api.route('/chat/<int:chat_id>', methods=['GET'])
def get_chat(chat_id):
    chat = chats.get(chat_id)
    if not chat:
        return jsonify({"message": "Chat not found"}), 404

    return jsonify({"chat_id": chat_id, "message": chat["message"], "user_id": chat["user_id"]}), 200

# API endpoint to fetch chat history between two users
@app.route('/api/chat/<user1>/<user2>', methods=['GET'])
def get_chat_history(user1, user2):
    chat_history = [
        chat for chat in chats.values()
        if str(chat["user_id"]) in [user1, user2]
    ]
    if not chat_history:
        return jsonify({"message": "No chat history found"}), 200

    return jsonify(chat_history), 200


# if __name__ == "__main__":
#     # change name for testing
#     app.run(debug=True, host="0.0.0.0", port="8887")