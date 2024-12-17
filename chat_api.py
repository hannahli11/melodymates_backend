from flask import Flask, jsonify, request
from flask_cors import CORS

# Initialize a Flask application
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

# In-memory database for user information
InfoDb = [
    {"FirstName": "Hannah", "LastName": "Li", "Username": "Hannahli_11"},
    {"FirstName": "Carson", "LastName": "Sutherland", "Username": "CJSuth$"},
    {"FirstName": "Rhea", "LastName": "Rajashekhar", "Username": "rhear$"},
    {"FirstName": "Brandon", "LastName": "Smurlo", "Username": "bsmurlo"},
    {"FirstName": "Rowan", "LastName": "Sutherland", "Username": "rowangs.1"}
]

# API endpoint to fetch all users
@app.route('/api/users', methods=['GET'])
def get_all_users():
    return jsonify(InfoDb)

# API endpoint to fetch a user by their username
@app.route('/api/user/<username>', methods=['GET'])
def get_user_by_username(username):
    user = next((u for u in InfoDb if u["Username"] == username), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# API endpoint to add a new user
@app.route('/api/user', methods=['POST'])
def add_user():
    data = request.json
    if not data or "FirstName" not in data or "LastName" not in data or "Username" not in data:
        return jsonify({"error": "Invalid input"}), 400

    # Check for duplicates
    if any(u["Username"] == data["Username"] for u in InfoDb):
        return jsonify({"error": "Username already exists"}), 409

    InfoDb.append({
        "FirstName": data["FirstName"],
        "LastName": data["LastName"],
        "Username": data["Username"]
    })
    return jsonify({"message": "User added successfully"}), 201

# HTML root endpoint
@app.route('/')
def say_hello():
    html_content = """
    <html>
    <head>
        <title>Chat Backend</title>
    </head>
    <body>
        <h2>Welcome to the Chat Backend API!</h2>
        <p>Endpoints:</p>
        <ul>
            <li>/api/users - GET all users</li>
            <li>/api/user/&lt;username&gt; - GET user by username</li>
            <li>/api/user - POST to add a new user</li>
        </ul>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    # Start Flask server on http://127.0.0.1:5001
    app.run(port=5001)
