import openai
import speech_recognition as sr
import pyttsx3
from flask import Flask, request, jsonify
import datetime

# Initialize Flask App
app = Flask(__name__)

# Set your API key
OPENAI_API_KEY = "OpenAi API Key"  # Replace with your OpenAI API key

# Initialize OpenAI client
client = openai.Client(api_key=OPENAI_API_KEY)

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# -------------------------------
# 📌 1. Chatbot (OpenAI Chat API)
# -------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# 📌 2. Get Current Time
# -------------------------------
@app.route("/time", methods=["GET"])
def get_time():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"time": now})

# -------------------------------
# 📌 3. Speech-to-Text (Voice Input)
# -------------------------------
@app.route("/speech_to_text", methods=["POST"])
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return jsonify({"transcription": text})

        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand audio"}), 400
        except sr.RequestError:
            return jsonify({"error": "Speech recognition service unavailable"}), 500

# -------------------------------
# 📌 4. Text-to-Speech (AI Reads Text)
# -------------------------------
@app.route("/text_to_speech", methods=["POST"])
def text_to_speech():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Text cannot be empty"}), 400

    try:
        engine.say(text)
        engine.runAndWait()
        return jsonify({"message": "Speech played successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# 🚀 Run Flask Server
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
