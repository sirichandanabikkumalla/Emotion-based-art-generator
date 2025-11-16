📌 Emotion-Based Art Generator – Backend
This is the backend API for the Emotion-Based Art Generator project.
It provides:

User Signup

User Login

JWT Authentication

Emotion Detection using a HuggingFace model

Returns AI-mapped artwork based on emotion

The frontend team can call these APIs to authenticate users and generate emotion-based art.

🚀 Tech Stack
Python

Flask

SQLite

JWT Authentication

Transformers (HuggingFace)

📁 Project Structure
cpp
Copy code
emotion-based-art-generator/
│── app.py
│── requirements.txt
│── static/
│     └── art/
│          ├── happy.jpg
│          ├── sad.jpg
│          ├── angry.jpg
│          ├── calm.jpg
│          └── ...etc
⚙️ Installation
1️⃣ Create a virtual environment (optional):
nginx
Copy code
python -m venv venv
venv\Scripts\activate
2️⃣ Install dependencies:
nginx
Copy code
pip install -r requirements.txt
3️⃣ Run the server:
nginx
Copy code
python app.py
Backend will start at:

cpp
Copy code
http://127.0.0.1:5000
🔐 Authentication Flow
User signs up → /signup

User logs in → /login

Backend returns a JWT token

Frontend stores token and uses it in:

makefile
Copy code
Authorization: Bearer <token>
📌 Available APIs
1. Signup
POST /signup
Request Body
json
Copy code
{
  "email": "test@gmail.com",
  "password": "123456"
}
Success Response
json
Copy code
{
  "message": "Account created successfully"
}
Error Response
json
Copy code
{
  "error": "Email already exists"
}
2. Login
POST /login
Request Body
json
Copy code
{
  "email": "test@gmail.com",
  "password": "123456"
}
Success Response
json
Copy code
{
  "token": "JWT_TOKEN_HERE",
  "message": "Login successful"
}
Error Response
json
Copy code
{
  "error": "Invalid email or password"
}
3. Analyze Emotion (Protected Route)
POST /analyze_text
Headers Required
pgsql
Copy code
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
Request Body
json
Copy code
{
  "text": "I feel very happy today"
}
Success Response
json
Copy code
{
  "emotion": "happy",
  "art_url": "/static/art/happy.jpg"
}
Error Response
json
Copy code
{
  "error": "No text provided"
}
🧪 Testing with Postman
Import this collection JSON
Copy this and save as EmotionArt.postman_collection.json, then import into Postman.

✅ 2. POSTMAN COLLECTION JSON
json
Copy code
{
  "info": {
    "name": "Emotion Art API",
    "_postman_id": "f48f5fe1-b2df-4f5d-a37a-123abcd987ef",
    "description": "Postman collection for Emotion-Based Art Generator backend",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Signup",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n    \"email\": \"test@gmail.com\",\n    \"password\": \"123456\"\n}"
        },
        "url": {
          "raw": "http://127.0.0.1:5000/signup",
          "protocol": "http",
          "host": ["127", "0", "0", "1"],
          "port": "5000",
          "path": ["signup"]
        }
      }
    },
    {
      "name": "Login",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n    \"email\": \"test@gmail.com\",\n    \"password\": \"123456\"\n}"
        },
        "url": {
          "raw": "http://127.0.0.1:5000/login",
          "protocol": "http",
          "host": ["127", "0", "0", "1"],
          "port": "5000",
          "path": ["login"]
        }
      }
    },
    {
      "name": "Analyze Text (Protected)",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer {{token}}"
          },
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n    \"text\": \"I feel so happy today\"\n}"
        },
        "url": {
          "raw": "http://127.0.0.1:5000/analyze_text",
          "protocol": "http",
          "host": ["127", "0", "0", "1"],
          "port": "5000",
          "path": ["analyze_text"]
        }
      }
    }
  ]
}
🎯 3. How to Use the Postman Collection
Step 1 → Import JSON file
Click:
Postman → Import → File → select JSON

Step 2 → Signup a test user
Run the Signup request.

Step 3 → Login
Run Login → copy the "token" from response.

Step 4 → Set Token in Collection Variable
In Postman:

bash
Copy code
Variables → token → paste it
Step 5 → Run Analyze API
Now it will work.
