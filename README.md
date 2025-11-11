# 🎨 Emotion-Based Art Generator

This project is a **Emotion based art generator Web App** that analyzes user input (text or voice) and displays an artwork corresponding to the detected emotion.  
It uses a **Transformer-based NLP model** (`j-hartmann/emotion-english-distilroberta-base`) for emotion recognition.

---

## 🌈 Features
- 🎤 **Voice Input** and ✍️ **Text Input** support  
- 🧠 Detects emotions using a fine-tuned transformer model  
- 🖼 Displays corresponding emotion-based art images  
- 🌐 Ready to connect with a separate frontend (React / HTML)  
- ☁️ Fully deployable on **Render**

## 🧩 Tech Stack
- **Backend:** Flask (Python)
- **Model:** Hugging Face Transformers
- **Frontend Template:** HTML + JavaScript (for text & voice input)
- **Deployment:** Render (Free Plan)
- **Language:** Python 3.12

## 🧠 Emotion Categories
| Emotion | Artwork File |
|----------|---------------|
| Happy | `happy.png` |
| Sad | `sad.png` |
| Angry | `angry.png` |
| Fear | `fear.png` |
| Love | `love.png` |
| Surprise | `surprise.png` |
| Disgust | `disgust.png` |
| Calm / Neutral | `calm.png` |

## ⚙️ Setup Instructions (for Developers)

### 1️⃣ Clone this Repository
```bash
git clone https://github.com/<your-username>/emotion-art-backend.git
cd emotion-art-backend
Install Dependencies
pip install -r requirements.txt

3️⃣ Run the Flask App
python app.py


Then open http://localhost:5000
 in your browser 🎨

☁️ Deployment on Render

Go to https://render.com

Click New + → Web Service

Connect this GitHub repository

In Build Command, leave it blank

In Start Command, enter:

python app.py


Select Free Plan → Deploy 🚀

After deployment, you’ll get a live URL like:

https://emotion-art-backend.onrender.com


Use this URL in your frontend to call the API:

POST /analyze_text


Example request:

fetch("https://emotion-art-backend.onrender.com/analyze_text", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text: "I feel wonderful today!" })
})

📂 Project Structure
emotionbasedartgenerator/
│
├── app.py
├── requirements.txt
├── runtime.txt
├── templates/
│   └── index.html
└── static/
    └── art/
        ├── happy.png
        ├── sad.png
        ├── angry.png
        ├── fear.png
        ├── love.png
        ├── surprise.png
        ├── disgust.png
        └── calm.png

🧠 API Endpoint
POST /analyze_text

Request Body:

{
  "text": "I am feeling joyful today!"
}


Response:

{
  "emotion": "joy",
  "art_url": "/static/art/happy.png"
}

💡 Notes

Make sure torch and transformers are installed properly (Render may take 3–4 mins to build).

Use flask-cors to allow frontend API access.

The app automatically loads and caches the transformer model for faster responses.

👩‍🎨 Author

Developed by Siri Chandana ✨
GitHub Profile
