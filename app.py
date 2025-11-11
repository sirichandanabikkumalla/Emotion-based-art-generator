from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY", "devkey123")

app = Flask(__name__)

# ensure static/art exists
os.makedirs(os.path.join(app.root_path, "static", "art"), exist_ok=True)

# Map model emotions → artwork filenames (png)
emotion_art = {
    "joy": "happy.png",        # ✅ added line
    "happy": "happy.png",      # (keep for future safety)
    "sadness": "sad.png",
    "anger": "angry.png",
    "fear": "fear.png",
    "love": "love.png",
    "surprise": "surprise.png",
    "disgust": "disgust.png",
    "neutral": "calm.png"
}

# Lazy-loaded model container
_emotion_model = None

def get_emotion_model():
    global _emotion_model
    if _emotion_model is None:
        try:
            print("Loading emotion model... (this may take a while)")
            from transformers import pipeline
            _emotion_model = pipeline(
                "text-classification", model="j-hartmann/emotion-english-distilroberta-base"
            )
            print("Emotion model loaded successfully.")
        except Exception as e:
            # keep _emotion_model as None and log error
            print("Failed to load emotion model:", e)
            traceback.print_exc()
            _emotion_model = None
    return _emotion_model

# -----------------------
# Home route
# -----------------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# -----------------------
# Analyze text endpoint
# -----------------------
@app.route("/analyze_text", methods=["POST"])
def analyze_text():
    data = request.json or {}
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    model = get_emotion_model()
    if model is None:
        # Model failed to load — return a friendly error
        return jsonify({
            "error": "Emotion model is not available. Server could not load it. Check server logs."
        }), 503

    try:
        result = model(text)
        # result may be list like [{'label': 'happy', 'score': 0.98}]
        if isinstance(result, list) and result:
            label = result[0].get("label", "")
        elif isinstance(result, dict):
            label = result.get("label", "")
        else:
            label = str(result)
        print(">>> Model raw result:", result)
        print(">>> Detected emotion label:", label)

        emotion = label.lower()
        art_file = emotion_art.get(emotion, "calm.png")
        art_url = f"/static/art/{art_file}"
        
        return jsonify({"emotion": emotion, "art_url": art_url})
    except Exception as e:
        print("Error during prediction:", e)
        traceback.print_exc()
        return jsonify({"error": "Prediction error. See server logs."}), 500

if __name__ == "__main__":
    # Use host=0.0.0.0 if you want the app to be reachable from other devices on the network
    # Leave debug=True for development (shows useful tracebacks in terminal)
    app.run(debug=True, host="0.0.0.0", port=5000)
