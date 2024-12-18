from flask import Flask, Blueprint, jsonify, request
from flask_restful import Api, Resource  # used for REST API building
from flask_cors import CORS

# Initialize a Flask application
musicChat_api = Blueprint('musicChat_api', __name__, url_prefix='/api')
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(musicChat_api)

# In-memory database for active users and chats
active_users = []  # Users who are currently logged in
chats = {}  # Dictionary to store chats between users

# API endpoint to fetch all active users
@app.route('/api/users', methods=['GET'])
def get_all_users():
    return jsonify(active_users)

# API endpoint to log in a user
@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.json
    if not data or "Username" not in data:
        return jsonify({"error": "Invalid input"}), 400

    username = data["Username"]
    # Add user to active users if not already present
    if username not in active_users:
        active_users.append(username)
    return jsonify({"message": f"{username} logged in successfully"}), 200

# API endpoint to log out a user
@app.route('/api/logout', methods=['POST'])
def logout_user():
    data = request.json
    if not data or "Username" not in data:
        return jsonify({"error": "Invalid input"}), 400

    username = data["Username"]
    if username in active_users:
        active_users.remove(username)
    return jsonify({"message": f"{username} logged out successfully"}), 200

# API endpoint to send a message
@app.route('/api/chat', methods=['POST'])
def send_message():
    data = request.json
    if not data or "sender" not in data or "receiver" not in data or "message" not in data:
        return jsonify({"error": "Invalid input"}), 400

    sender = data["sender"]
    receiver = data["receiver"]
    message = data["message"]

    # Ensure sender and receiver are valid
    if sender not in active_users or receiver not in active_users:
        return jsonify({"error": "Both sender and receiver must be logged in"}), 400

    # Create a unique key for the chat between sender and receiver
    chat_key = tuple(sorted([sender, receiver]))

    # Add message to the chat
    if chat_key not in chats:
        chats[chat_key] = []
    chats[chat_key].append({"sender": sender, "message": message})

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


class musicChatAPI:
   # @app.route('/api/student/')
    def get_user(name):
        users = {
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
                "TimeStamp" : "6:05"
            },
            "Rowan": {
                "Username": "rowangs",
                "MessageStatus" : "sent",
                "TimeStamp" : "4:58",
            },
             "Brandon": {
                "Username": "bsmurlo",
                "MessageStatus" : "read",
                "TimeStamp" : "11:11"
            }
        }
        return users[name]
    
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

