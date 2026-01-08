import os
import json
from flask import Flask, render_template, request
from model_interface import analyze_user_condition
import pyttsx3

# ------------------------------
# Paths
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "astronaut_data")
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

# ------------------------------
# TTS Setup
# ------------------------------
engine = pyttsx3.init()
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# ------------------------------
# Flask App
# ------------------------------
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # We'll create this next

@app.route("/submit", methods=["POST"])
def submit():
    form = request.form
    name = form.get("name", "").strip().lower()
    symptoms = [s.strip().lower() for s in form.get("symptoms", "").split(",") if s.strip()]

    if not name or not symptoms:
        return render_template("index.html", output="Please enter both name and symptoms.")

    # Collect vitals from form
    vitals = {
        "heart_rate": form.get("heart_rate"),
        "blood_pressure": form.get("blood_pressure"),
        "oxygen_saturation": form.get("oxygen_saturation"),
        "body_temperature": form.get("body_temperature"),
        "respiratory_rate": form.get("respiratory_rate"),
        "sleep_hours": form.get("sleep_hours"),
    }

    # Update JSON file
    user_file = os.path.join(DATA_PATH, f"{name}.json")
    if os.path.exists(user_file):
        with open(user_file, "r") as f:
            data = json.load(f)
    else:
        data = {"name": name, "vital_signs": {}, "recent_symptoms": []}

    data["vital_signs"].update(vitals)
    data["recent_symptoms"] = symptoms

    with open(user_file, "w") as f:
        json.dump(data, f, indent=4)

    # Run AI analysis
    try:
        response = analyze_user_condition(DATA_PATH, name, symptoms=symptoms)
        speak_text(response)  # Optional TTS on server
        return render_template("index.html", output=response)
    except Exception as e:
        return render_template("index.html", output=f"Analysis failed: {e}")

# ------------------------------
# Run App
# ------------------------------
if __name__ == "__main__":
    # Host=0.0.0.0 allows LAN access so iPad can connect
    app.run(host="0.0.0.0", port=5000, debug=True)