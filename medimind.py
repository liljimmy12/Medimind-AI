
import os
import json

folder_path = "/home/meyerj@CSGP.EDU/https:/github.com/liljimmy12/Mediming-AI.git"

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

