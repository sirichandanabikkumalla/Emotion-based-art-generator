from flask import Flask, request, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_cors import CORS
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------------
# Flask App Initialization
# ------------------------------
app = Flask(__name__, static_folder="static", template_folder="templates")

# ------------------------------
# Config
# ------------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecretkey")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

CORS(app, resources={r"/*": {
    "origins": [
        "http://127.0.0.1:5000",
        "http://localhost:5000",
        "http://127.0.0.1:5500"
    ],
    "supports_credentials": True,
    "allow_headers": ["Content-Type", "Authorization"],
    "expose_headers": ["Content-Type", "Authorization"],
    "methods": ["GET", "POST", "OPTIONS"]
}})

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ------------------------------
# User Model
# ------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

# ------------------------------
# Emotion Art Mapping
# ------------------------------
emotion_art = {
    "happy": "happy.PNG",
    "sadness": "sad.PNG",
    "anger": "angry.PNG",
    "fear": "fear.PNG",
    "love": "love.PNG",
    "surprise": "surprise.PNG",
    "disgust": "disgust.PNG",
    "neutral": "calm.PNG"
}

# ------------------------------
# Load Emotion Model
# ------------------------------
try:
    from transformers import pipeline
    emotion_model = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base"
    )
except Exception:
    emotion_model = None

# ------------------------------
# Simple Fallback Model
# ------------------------------
def demo_guess(text: str) -> str:
    t = (text or "").lower()
    if any(w in t for w in ["happy", "joy", "glad", "excited", "yay"]): return "happy"
    if any(w in t for w in ["sad", "tear", "cry", "depress"]): return "sadness"
    if any(w in t for w in ["angry", "mad", "furious", "hate"]): return "anger"
    if any(w in t for w in ["fear", "scared", "afraid", "nervous"]): return "fear"
    if any(w in t for w in ["love", "heart", "romantic"]): return "love"
    if any(w in t for w in ["surprise", "wow", "shocked"]): return "surprise"
    if any(w in t for w in ["disgust", "gross", "yuck"]): return "disgust"
    return "neutral"

# ------------------------------
# Emotion-Aware Responses ❤️
# ------------------------------
emotion_responses = {
    "happy": "That's wonderful! Keep smiling and spreading joy ✨",
    "sadness": "It’s okay to feel sad… your emotions are valid. I’m here with you 💛",
    "anger": "Take a deep breath. You deserve peace and calm 🕊️",
    "fear": "You are stronger than your fears — believe in yourself 🌟",
    "love": "Your heart is full — cherish this beautiful feeling ❤️",
    "surprise": "Omg! Something unexpected happened, right? 🎉",
    "disgust": "It’s okay to step away from things that don’t feel right 🤍",
    "neutral": "Feeling balanced and calm is a beautiful space 🌿"
}

# ------------------------------
# Page Routes
# ------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/auth.html")
def auth_page():
    return render_template("auth.html")

@app.route("/chat.html")
def chat_page():
    return render_template("chat.html")

# ------------------------------
# Signup Route
# ------------------------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email & Password required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(email=email, password=hashed_pw)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Signup successful"}), 201

# ------------------------------
# Login Route
# ------------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({"token": token}), 200

# ------------------------------
# Emotion Analysis Route
# ------------------------------
@app.route("/analyze_text", methods=["POST"])
@jwt_required()
def analyze_text():

    _ = get_jwt_identity()  # Validate JWT

    data = request.get_json()
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "Text is required"}), 400

    # Detect emotion using real or fallback model
    try:
        if emotion_model:
            result = emotion_model(text)[0]
            raw = (result["label"] or "").lower()

            mapping = {
                "joy": "happy",
                "sadness": "sadness",
                "anger": "anger",
                "fear": "fear",
                "love": "love",
                "surprise": "surprise",
                "disgust": "disgust",
                "neutral": "neutral"
            }

            emotion = mapping.get(raw, "neutral")
        else:
            emotion = demo_guess(text)

    except Exception:
        emotion = demo_guess(text)

    # Build art URL
    art_file = emotion_art.get(emotion, "calm.PNG")
    art_url = url_for("static", filename=f"art/{art_file}")

    # Return output
    return jsonify({
        "emotion": emotion,
        "art_url": art_url,
        "response": emotion_responses.get(emotion, "")
    }), 200

# ------------------------------
# Run Server
# ------------------------------
if __name__ == "__main__":
    os.makedirs("static/art", exist_ok=True)
    app.run(debug=True)
