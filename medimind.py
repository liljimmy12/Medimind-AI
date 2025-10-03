
import os
import json
import torch
from transformers import pipeline

folder_path = "/home/meyerj@CSGP.EDU/Medimind-AI"

generator = pipeline(
    task="text-generation",
    model="microsoft/biogpt",
    dtype=torch.float16,
    device=0,
)

NASA_MISSION_CONTEXT = (
    "the AI-driven medical diagnosis system for long-duration space Missions "
    "supports astronaut health during Moon and Mars expeditions. "
    "communication delays and blackouts make earth-based medical support infeasible. "
    "the system gathers biosensor and crew input, delivering actionable guidance. "
    "crew have limited medical training and must operate autonomously. "
    "vital signs, symptoms, medications, mission environment, radiation exposure, "
    "and microgravity experience are all important factors."
)

ALERTS = {
    "oxygen_saturation": 90,    
    "heart_rate_low": 50,       
    "heart_rate_high": 110,    
    "radiation_exposure": 100, 
}

def user_management_system():
    action = input("do you want to 'load', 'add', 'delete', 'update' a user? ").lower()
#add a JSON file
    if action == "add":
        name = input("enter your name: ").lower()
        age = input("enter your age: ").lower()
        sex = input("enter your sex M/F/O: ").lower()
        height = input("enter your height: ").lower()
        weight = input("enter your weight in lb: ").lower()
        crew_role = input("enter your crew role: ").lower()
        blood_type = input("enter your blood type: ").lower()
        allergies = input("enter allergies (comma-separated): ").lower().split(",") if input("any allergies? (y/n): ").lower() == "y" else []
        chronic_conditions = input("enter chronic conditions (comma-separated): ").lower().split(",") if input("any chronic conditions? (y/n): ").lower() == "y" else []

    #vital signs
        heart_rate = input("enter heart rate (bpm): ").lower()
        blood_pressure = input("enter blood pressure (systolic/diastolic): ").lower()
        oxygen_saturation = input("enter oxygen saturation (%): ").lower()
        body_temperature = input("enter body temperature (°C): ").lower()
        respiratory_rate = input("enter respiratory rate (breaths per min): ").lower()
        sleep_hours = input("average sleep hours per day: ").lower()

    # Current symptoms and medication
        recent_symptoms = input("enter recent symptoms (comma-separated): ").lower().split(",") if input("any recent symptoms? (y/n): ").lower() == "y" else []
        medications = input("enter medications (comma-separated): ").lower().split(",") if input("any medications? (y/n): ").lower() == "y" else []
        vaccinations = input("enter vaccinations (comma-separated): ").lower().split(",") if input("any vaccinations? (y/n): ").lower() == "y" else []

    # Mission-specific data
        current_location = input("current location (e.g., moon base): ").lower()
        radiation_exposure = input("radiation exposure (mSv): ").lower()
        microgravity_days = input("microgravity experience (days): ").lower()
        exercise_minutes = input("exercise per day (minutes): ").lower()

    #preferences
        preferred_language = input("preferred language: ").lower()
        alert_contacts = input("alert contacts (comma-separated emails): ").lower().split(",") if input("any alert contacts? (y/n): ").lower() == "y" else []

        user_info = {
            "name": name,
            "age": age,
            "sex": sex,
            "height": height,
            "weight": weight,
            "crew_role": crew_role,
            "blood_type": blood_type,
            "allergies": allergies,
            "chronic_conditions": chronic_conditions,
            "vital_signs": {
                "heart_rate": heart_rate,
                "blood_pressure": blood_pressure,
                "oxygen_saturation": oxygen_saturation,
                "body_temperature": body_temperature,
                "respiratory_rate": respiratory_rate,
                "sleep_hours": sleep_hours
            },
            "recent_symptoms": recent_symptoms,
            "medications": medications,
            "vaccinations": vaccinations,
            "mission_data": {
                "current_location": current_location,
                "radiation_exposure": radiation_exposure,
                "microgravity_experience_days": microgravity_days,
                "exercise_minutes_per_day": exercise_minutes
            },
            "preferences": {
                "preferred_language": preferred_language,
                "alert_contacts": alert_contacts,
            }
        }

        file_path = os.path.join(folder_path, f"{name}.json")
        with open(file_path, "w") as file:
            json.dump(user_info, file, indent=4)

        print(f"Information saved to {file_path}")
#load data of JSON file
    elif action == "load":
        name_to_load = input("enter the name of the user you want to load: ").lower()
        file_path = os.path.join(folder_path, f"{name_to_load}.json")

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                loaded_info = json.load(file)

            print("\nloaded user info:")
            for key, value in loaded_info.items():
                print(f"{key}: {value}")
        else:
            print(f"no information found for '{name_to_load}'.")
#delete a JSON file
    elif action == "delete":
        name_to_delete = input("enter the name of the user you want to delete: ").lower()
        file_path = os.path.join(folder_path, f"{name_to_delete}.json")
    
        if os.path.exists(file_path):
            confirm = input(f"Are you sure you want to delete '{name_to_delete}'? Type 'yes' to confirm: ").lower()
            if confirm == "yes":
                os.remove(file_path)
                print(f"user '{name_to_delete}' has been deleted.")
            else:
                print("deletion canceled.")
#update a JSON file
    elif action == "update":
        name_to_update = input("enter the name of the user you want to update: ").lower()
        file_path = os.path.join(folder_path, f"{name_to_update}.json")

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                user_info = json.load(file)

            print("\npress enter to keep current value.")

        
            def default_value(field):
                if field in ["allergies", "chronic_conditions", "recent_symptoms", "medications", "vaccinations", "alert_contacts"]:
                    return []
                elif field in ["vital_signs", "mission_data", "preferences"]:
                    return {}
                else:
                    return ""

            def update_field(field, subfield=None):
            
                if field not in user_info:
                    user_info[field] = default_value(field)

                if subfield:
                    if subfield not in user_info[field]:
                        user_info[field][subfield] = ""
                    current_value = user_info[field][subfield]
                    new_value = input(f"{subfield} ({current_value}): ").lower()
                    if new_value:
                        user_info[field][subfield] = new_value
                else:
                    current_value = user_info[field]
                    if isinstance(current_value, list):
                        print(f"{field} current: {', '.join(current_value)}")
                        new_value = input(f"Update {field} (comma-separated, leave blank to keep): ").lower()
                        if new_value:
                            user_info[field] = [v.strip() for v in new_value.split(",")]
                    else:
                        new_value = input(f"{field} ({current_value}): ").lower()
                        if new_value:
                            user_info[field] = new_value

        
            for key in ["name", "age", "sex", "height", "weight", "crew_role", "blood_type"]:
                update_field(key)

            for key in ["allergies", "chronic_conditions", "recent_symptoms", "medications", "vaccinations", "alert_contacts"]:
                update_field(key)

            for subfield in ["heart_rate", "blood_pressure", "oxygen_saturation", "body_temperature", "respiratory_rate", "sleep_hours"]:
                update_field("vital_signs", subfield)

            for subfield in ["current_location", "radiation_exposure", "microgravity_experience_days", "exercise_minutes_per_day"]:
                update_field("mission_data", subfield)

            for subfield in ["preferred_language"]:
                update_field("preferences", subfield)

            with open(file_path, "w") as file:
                json.dump(user_info, file, indent=4)
            print(f"user '{name_to_update}' has been updated.")

        else:
            print(f"no information found for '{name_to_update}'.")


    else:
        print("invalid action. Please type 'load', 'add', 'delete', or 'update'.")


#BioGPT and diagnostic
def batch_analyze_with_alerts():
    json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]
    if not json_files:
        print("No astronaut data found.")
        return

    for file_name in json_files:
        with open(os.path.join(folder_path, file_name), "r") as file:
            data = json.load(file)

        name = data.get("name", file_name.replace(".json", "Unknown"))
        vitals = data.get("vital_signs", {})
        mission = data.get("mission_data", {})

        summary = []
        summary.append(f"Heart rate: {vitals.get('heart_rate', 'N/A')} bpm")
        summary.append(f"Blood pressure: {vitals.get('blood_pressure', 'N/A')}")
        summary.append(f"Oxygen saturation: {vitals.get('oxygen_saturation', 'N/A')}%")
        summary.append(f"Body temperature: {vitals.get('body_temperature', 'N/A')} °C")
        summary.append(f"Respiratory rate: {vitals.get('respiratory_rate', 'N/A')} breaths/min")
        summary.append(f"Sleep: {vitals.get('sleep_hours', 'N/A')} hrs/day")
        summary.append(f"Symptoms: {', '.join(data.get('recent_symptoms', [])) or 'None'}")
        summary.append(f"Medications: {', '.join(data.get('medications', [])) or 'None'}")
        summary.append(f"Location: {mission.get('current_location', 'N/A')}")
        summary.append(f"Radiation exposure: {mission.get('radiation_exposure', 'N/A')} mSv")
        summary.append(f"Microgravity experience: {mission.get('microgravity_experience_days', 'N/A')} days")
        summary.append(f"Exercise minutes/day: {mission.get('exercise_minutes_per_day', 'N/A')} minutes")

        # Check alerts
        alert_messages = []
        try:
            if float(vitals.get("oxygen_saturation", 100)) < ALERTS["oxygen_saturation"]:
                alert_messages.append("Oxygen saturation below safe threshold!")
            hr = float(vitals.get("heart_rate", 80))
            if hr < ALERTS["heart_rate_low"] or hr > ALERTS["heart_rate_high"]:
                alert_messages.append("Heart rate outside normal range!")
            if float(mission.get("radiation_exposure", 0)) > ALERTS["radiation_exposure"]:
                alert_messages.append("Radiation exposure high!")
        except ValueError:
            pass  # Ignore non-numeric values

        prompt = (
            f"{NASA_MISSION_CONTEXT}\n\n"
            f"Astronaut: {name}\n"
            "Medical summary:\n" + "\n".join(summary) + "\n"
            f"Alerts: {', '.join(alert_messages) if alert_messages else 'None'}\n"
            "Provide AI-generated insights relevant to long-duration space missions. "
            "Do NOT prescribe medications."
        )

        result = generator(prompt, truncation=True, max_length=250, do_sample=True)[0]["generated_text"]
        print(f"\n=== BioGPT Insights for {name} ===")
        print(result)
        print("\n" + "="*80 + "\n")




entry = input("choose which system you would like to use: /n"
"1 > user management"
"2 > diagnosis analyzer")
if entry == "1":
    user_management_system()
if entry == "2":
    batch_analyze_with_alerts()
else:
    print("Access denied. You did not type a system.")


