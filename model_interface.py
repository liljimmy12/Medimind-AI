import os
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "BioMedLM")

# Load tokenizer and model from local folder
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16, device_map="auto")

generator = pipeline(
    task="text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0
)

NASA_CONTEXT = (
    "AI-driven medical decision-support for astronauts on long-duration space missions. "
    "Crew have limited supplies and delayed Earth communication. "
    "The model provides educational guidance and procedural advice only, "
    "not actual medical prescriptions."
)

def load_all_crew_data(folder_path):
    """Load all astronaut JSON files."""
    crew_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), "r") as f:
                try:
                    data = json.load(f)
                    crew_data.append((data.get("name", filename[:-5]), data))
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    return crew_data

def summarize_crew_health(crew_data):
    """Create a summary of crew vitals and symptoms."""
    summaries = []
    for name, data in crew_data:
        vitals = data.get("vital_signs", {})
        symptoms = ", ".join(data.get("recent_symptoms", [])) or "none"
        rad = data.get("mission_data", {}).get("radiation_exposure", "N/A")
        summaries.append(
            f"{name}: HR {vitals.get('heart_rate', 'N/A')} bpm, "
            f"O2 {vitals.get('oxygen_saturation', 'N/A')}%, "
            f"Temp {vitals.get('body_temperature', 'N/A')}°C, "
            f"Symptoms: {symptoms}, Radiation: {rad} mSv."
        )
    return "\n".join(summaries)

def collect_user_symptoms():
    """Ask the astronaut for structured symptoms and free-text description."""
    print("\nEnter your symptoms one by one. Press Enter when finished.")
    symptoms = []
    while True:
        s = input("Symptom: ").strip().lower()
        if not s:
            break
        symptoms.append(s)

    free_text = input("\nDescribe how you feel in your own words (optional): ").strip()
    combined_message = ""
    if symptoms:
        combined_message += "Reported symptoms: " + ", ".join(symptoms) + ". "
    combined_message += free_text
    return combined_message, symptoms

def analyze_user_condition(folder_path, user_name):
    """Generate AI guidance using user data and crew cross-referencing."""
    user_file = os.path.join(folder_path, f"{user_name.lower()}.json")
    if not os.path.exists(user_file):
        print(f"No data found for '{user_name}'. Please add your profile first.")
        return

    with open(user_file, "r") as f:
        user_data = json.load(f)

    crew_data = load_all_crew_data(folder_path)
    crew_context = summarize_crew_health(crew_data)

    message, structured_symptoms = collect_user_symptoms()

    # Update user's recent symptoms in JSON
    if structured_symptoms:
        user_data["recent_symptoms"] = structured_symptoms
        with open(user_file, "w") as f:
            json.dump(user_data, f, indent=4)

    vitals = user_data.get("vital_signs", {})
    individual_summary = (
        f"Astronaut: {user_name}\n"
        f"Heart rate: {vitals.get('heart_rate', 'N/A')} bpm\n"
        f"Oxygen saturation: {vitals.get('oxygen_saturation', 'N/A')}%\n"
        f"Radiation exposure: {user_data.get('mission_data', {}).get('radiation_exposure', 'N/A')} mSv\n"
        f"Previous symptoms: {', '.join(user_data.get('recent_symptoms', [])) or 'None'}\n"
        f"User message: {message}\n"
    )

    prompt = (
        f"{NASA_CONTEXT}\n\n"
        f"=== Crew Health Overview ===\n{crew_context}\n\n"
        f"=== Subject Analysis ===\n{individual_summary}\n"
        "Analyze the user's condition relative to crew health patterns. "
        "Identify possible shared risk factors, environmental causes, or early signs "
        "of mission-wide medical issues. Suggest procedural or self-monitoring actions "
        "(no drugs, no prescriptions)."
    )

    response = generator(prompt, truncation=True, max_length=40,,../////////////////////////???///////////////////////'''0, do_sample=True)[0]["generated_text"]
    print(f"\n=== BioMedLM Crew-Cross Analysis for {user_name} ===\n")
    print(response)
    print("\n" + "="*80 + "\n")
