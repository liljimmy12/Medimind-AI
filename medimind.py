
import os
import json

folder_path = "/home/meyerj@CSGP.EDU/Medimind-AI"

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
        confirm = input(f"are you sure you want to delete '{name_to_delete}'? type 'yes' to confirm: ").lower()
        if confirm == "yes":
            os.remove(file_path)
            print(f"user '{name_to_delete}' has been deleted.")
        else:
            print("deletion canceled.")
    else:
        print(f"no information found for '{name_to_delete}'.")
#update a JSON file
elif action == "update":
    name_to_update = input("enter the name of the user you want to update: ").lower()
    file_path = os.path.join(folder_path, f"{name_to_update}.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            user_info = json.load(file)

        print("\npress enter to keep current value.")
        def update_field(field, subfield=None):
            if subfield:
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
        for subfield in ["preferred_language", "decision_preference"]:
            update_field("preferences", subfield)

        with open(file_path, "w") as file:
            json.dump(user_info, file, indent=4)
        print(f"user '{name_to_update}' has been updated.")

    else:
        print(f"no information found for '{name_to_update}'.")


else:
    print("invalid action. Please type 'load', 'add', or 'delete'.")

