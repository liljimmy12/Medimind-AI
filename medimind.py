
import os
import json

folder_path = "/home/meyerj@CSGP.EDU/Medimind-AI"

name_to_load = input("Enter the name of the user you want to load (type 'add' to add a new user): ").lower()

if name_to_load == "add":

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

else:
    file_path = os.path.join(folder_path, f"{name_to_load}.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            loaded_info = json.load(file)

        print("\nLoaded user info:")
        for key, value in loaded_info.items():
            print(f"{key}: {value}")
    else:
        print(f"No information found for '{name_to_load}'. Make sure the name is correct.")