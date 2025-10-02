
import os
import json

folder_path = "/home/meyerj@CSGP.EDU/Medimind-AI"

name = input("enter your name: ").lower()
age = input("enter your age: ").lower()
sex = input("enter your sex M/F/O: ").lower()
height = input("enter your height: ").lower()
weight = input("enter you weight in lb: ").lower()


user_info= {
    "name": name,
    "age": age,
    "sex": sex,
    "height": height,
    "weight": weight,
}

file_path = os.path.join(folder_path, f"{name}.json")

with open(file_path, "w") as file:
    json.dump(user_info, file, indent=4)

print(f"information saved to {file_path}")

name_to_load = input("Enter the name of the user you want to load: ").lower()

if os.path.exists(file_path):
    with open(file_path, "r") as file:
        loaded_info = json.load(file)

    print("\nLoaded user info:")
    for key, value in loaded_info.items():
        print(f"{key}: {value}")
else:
    print(f"No information found for '{name_to_load}'. Make sure the name is correct.")