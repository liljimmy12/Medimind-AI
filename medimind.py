
import os
import json

folder_path = "/home/meyerj@CSGP.EDU/Medimind-AI"

action = input("Do you want to 'load', 'add', or 'delete' a user? ").lower()

if action == "add":
    name = input("Enter your name: ").lower()
    age = input("Enter your age: ").lower()
    sex = input("Enter your sex M/F/O: ").lower()
    height = input("Enter your height: ").lower()
    weight = input("Enter your weight in lb: ").lower()

    user_info = {
        "name": name,
        "age": age,
        "sex": sex,
        "height": height,
        "weight": weight,
    }

    file_path = os.path.join(folder_path, f"{name}.json")
    with open(file_path, "w") as file:
        json.dump(user_info, file, indent=4)

    print(f"Information saved to {file_path}")

elif action == "load":
    name_to_load = input("Enter the name of the user you want to load: ").lower()
    file_path = os.path.join(folder_path, f"{name_to_load}.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            loaded_info = json.load(file)

        print("\nLoaded user info:")
        for key, value in loaded_info.items():
            print(f"{key}: {value}")
    else:
        print(f"No information found for '{name_to_load}'.")

elif action == "delete":
    name_to_delete = input("Enter the name of the user you want to delete: ").lower()
    file_path = os.path.join(folder_path, f"{name_to_delete}.json")

    if os.path.exists(file_path):
        confirm = input(f"Are you sure you want to delete '{name_to_delete}'? Type 'yes' to confirm: ").lower()
        if confirm == "yes":
            os.remove(file_path)
            print(f"User '{name_to_delete}' has been deleted.")
        else:
            print("Deletion canceled.")
    else:
        print(f"No information found for '{name_to_delete}'.")

else:
    print("Invalid action. Please type 'load', 'add', or 'delete'.")