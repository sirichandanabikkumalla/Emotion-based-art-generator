from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from transformers import pipeline
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------------
# Flask App Initialization
# ------------------------------

app = Flask(__name__)

# ------------------------------
# Database + JWT Configuration
# ------------------------------

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# JWT secret key
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecretkey")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ------------------------------
# User Model (User Management ORM)
# ------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

# ------------------------------
# Signup Route
# ------------------------------

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email & password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(email=email, password=hashed_pw)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Account created successfully"}), 201

# ------------------------------
# Login Route (Generates JWT Token)
# ------------------------------

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email & password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid password"}), 401

    token = create_access_token(identity=user.id)

    return jsonify({"token": token, "message": "Login successful"})

# ------------------------------
# Authentication Middleware Example
# ------------------------------

@app.route("/me", methods=["GET"])
@jwt_required()  # protects this route
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({"id": user.id, "email": user.email})

# ------------------------------
# Emotion Model and Art Mapping
# ------------------------------

emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
)

emotion_art = {
    "happy": "happy.jpg",
    "sadness": "sad.jpg",
    "anger": "angry.jpg",
    "fear": "fear.jpg",
    "love": "love.jpg",
    "surprise": "surprise.jpg",
    "disgust": "disgust.jpg",
    "neutral": "calm.jpg"
}

# ------------------------------
# Protected Emotion Analysis Route
# ------------------------------

@app.route("/analyze_text", methods=["POST"])
@jwt_required()
def analyze_text():
    data = request.json
    text = data.get("text")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = emotion_model(text)[0]
    emotion = result["label"].lower()

    art_file = emotion_art.get(emotion, "calm.jpg")
    art_url = f"/static/art/{art_file}"

    return jsonify({"emotion": emotion, "art_url": art_url})

# ------------------------------
# Run Server
# ------------------------------

if __name__ == "__main__":
    os.makedirs("static/art", exist_ok=True)
    app.run(debug=True)
