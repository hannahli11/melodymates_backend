from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Ensure uploads are in static directory
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store user data in memory (for demo purposes)
profiles = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('userprofile_setup.html')

@app.route('/api/submit_profile', methods=['POST'])
def submit_profile():
    name = request.form['name']
    bio = request.form['bio']
    artists = request.form['artists']
    no_picture = request.form.get('no_picture') == 'true'
    profile_picture = request.files.get('profile_picture')

    # Handle profile picture upload
    picture_url = None
    if profile_picture and allowed_file(profile_picture.filename):
        filename = secure_filename(profile_picture.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        profile_picture.save(file_path)
        picture_url = url_for('static', filename=f'uploads/{filename}')
    elif no_picture:
        picture_url = None
    else:
        return jsonify({"error": "Invalid file type or no file provided."}), 400

    # Store profile in memory
    profiles[name] = {
        "bio": bio,
        "artists": artists.split(','),
        "picture_url": picture_url
    }

    # Redirect to the profile page
    return redirect(url_for('view_profile', name=name))

@app.route('/profile/<name>')
def view_profile(name):
    profile = profiles.get(name)
    if not profile:
        return "Profile not found!", 404
    return render_template('profile.html', name=name, profile=profile)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
