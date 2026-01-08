from flask import Flask, render_template, request
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

# -----------------------------
# Load BioMedLM once at startup
# -----------------------------
MODEL_PATH = "~/.cache/huggingface/hub/models--stanford-crfm--BioMedLM" # adjust if your model folder is elsewhere

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

# Model
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)
model.eval()  # put model in evaluation mode

# -----------------------------
# Initialize Flask app
# -----------------------------
app = Flask(__name__)

# -----------------------------
# AI inference function
# -----------------------------
def generate_analysis(username, symptoms_list):
    """
    Takes a username and a list of symptoms,
    returns an AI-generated analysis from BioMedLM.
    """
    if not symptoms_list:
        return "No symptoms entered yet."
    
    # Join symptoms into a single string
    symptoms_text = ", ".join(symptoms_list)

    # Prompt for BioMedLM
    prompt = f"""
You are a helpful medical assistant.
A patient ({username}) reports the following symptoms: {symptoms_text}

Provide:
- Possible conditions (do NOT give a definitive diagnosis)
- General advice
- Urgency level (low / moderate / high)
End your response with a reminder to consult a licensed healthcare professional.
"""

    # Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt")

    # Generate model output
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=250,
            temperature=0.7,
            do_sample=True
        )

    # Decode output
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# -----------------------------
# Flask route for symptoms page
# -----------------------------
@app.route("/symptoms", methods=["GET", "POST"])
def symptoms():
    result = None
    username = request.cookies.get("username") or "test_user"
    
    if request.method == "POST":
        # Get raw text from form
        symptoms_raw = request.form.get("customSymptoms", "")
        # Split into a clean list
        symptoms_list = [s.strip() for s in symptoms_raw.split(",") if s.strip()]
        # Generate AI analysis
        result = generate_analysis(username, symptoms_list)
    
    return render_template("symptoms.html", result=result)

# -----------------------------
# Run the app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)

