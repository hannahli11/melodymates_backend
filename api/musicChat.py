from flask import Flask, Blueprint, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS

from model.musicChat import MusicChat


# Initialize a Flask application
musicChat_api = Blueprint('musicChat_api', __name__, url_prefix='/api/music_chat')
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

api = Api(musicChat_api)

# Simulating in-memory active users and chats for the sake of example
active_users = []  # Users who are currently logged in
chats = {}  # Dictionary to store chats between users

# API endpoint to send a message
@musicChat_api.route('/chat', methods=['POST']) # is endpoint to post a message on chatroom (POST METHOD)
def send_message(): # function to send messages defined
    data = request.json
    if not data or "message" not in data or "user_id" not in data:
        return jsonify({"error": "Invalid input"}), 400

    message = data["message"]
    user_id = data["user_id"]

   
    chat_id = len(chats) + 1  
    chats[chat_id] = {"message": message, "user_id": user_id}

    return jsonify({"message": "Message sent successfully"}), 200

# API endpoint to fetch chat history between two users
@app.route('/api/chat/<user1>/<user2>', methods=['GET'])
def get_chat_history(user1, user2):
    chat_key = tuple(sorted([user1, user2]))
    if chat_key in chats:
        return jsonify(chats[chat_key])
    return jsonify({"message": "No chat history found"}), 200

# HTML root endpoint
@app.route('/')
def say_hello():
    html_content = """
    <html>
    <head>
        <title>Music Chat Backend</title>
    </head>
    <body>
        <h2>Welcome to the Music Chat Backend API!</h2>
        <p>Endpoints:</p>
        <ul>
            <li>/api/users - GET all active users</li>
            <li>/api/login - POST to log in a user</li>
            <li>/api/logout - POST to log out a user</li>
            <li>/api/chat - POST to send a message</li>
            <li>/api/chat/&lt;user1&gt;/&lt;user2&gt; - GET chat history between two users</li>
        </ul>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    # Start Flask server on http://127.0.0.1:5001
    app.run(port=5001)

# Define all users as a dictionary
allUsers = {
    "Hannah": {
        "Username": "hannahli_11",
        "MessageStatus": "delivered",
        "TimeStamp": "11:33"
    },
    "Rhea": {
        "Username": "rhear_02",
        "MessageStatus": "sent",
        "TimeStamp": "3:21"
    },
    "Gaheera": {
        "Username": "gaheerb",
        "MessageStatus": "read",
        "TimeStamp": "8:40"
    },
    "Carson": {
        "Username": "carsonsuth17",
        "MessageStatus": "delivered",
        "TimeStamp": "6:05"
    },
    "Rowan": {
        "Username": "rowangs",
        "MessageStatus": "sent",
        "TimeStamp": "4:58"
    },
    "Brandon": {
        "Username": "bsmurlo",
        "MessageStatus": "read",
        "TimeStamp": "11:11"
    }
}
class musicChatAPI:
    def get_user():
        return allUsers
    
class HannahResource(Resource): 
    def get(self):
        user = musicChatAPI.get_user("Hannah")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
    
class RheaResource(Resource): 
     def get(self):
        user = musicChatAPI.get_user("Rhea")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
    
class RowanResource(Resource): 
      def get(self):
        user = musicChatAPI.get_user("Rowan")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
    
class GaheeraResource(Resource): 
      def get(self):
        user = musicChatAPI.get_user("Gaheera")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
class BrandonResource(Resource): 
      def get(self):
        user = musicChatAPI.get_user("Brandon")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
    
class CarsonResource(Resource): 
      def get(self):
        user = musicChatAPI.get_user("Carson")
        if user:
            return jsonify(user)
        return {"Data not found"}, 404
      
# Building REST API endpoint
api.add_resource(HannahResource, '/chat/Hannah')
api.add_resource(RheaResource, '/chat/Rhea')
api.add_resource(GaheeraResource, '/chat/Gaheera')
api.add_resource(RowanResource, '/chat/Rowan')
api.add_resource(CarsonResource, '/chat/Carson')
api.add_resource(BrandonResource, '/chat/Brandon')
api.add_resource(musicChatAPI, '/chat/allUsers')