import os
import sys
import zipfile
import subprocess
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
VOSK_DIR = os.path.join(MODELS_DIR, "vosk-model-small-en-us-0.15")
BIO_MODEL_DIR = os.path.join(MODELS_DIR, "BioMedLM")
VOSK_ZIP = os.path.join(MODELS_DIR, "vosk-model-small-en-us-0.15.zip")
DATA_DIR = os.path.join(BASE_DIR, "astronaut_data")

print("[*] Setting up offline Medimind environment...")

# ------------------------------
# 1. Directories
# ------------------------------
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# ------------------------------
# 2. Install dependencies
# ------------------------------
print("[*] Installing dependencies...")

packages = [
    "vosk",
    "sounddevice",
    "pyttsx3",
    "torch",
    "transformers",
    "accelerate",
    "safetensors",
    "sentencepiece",
    "flask"
]

try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", *packages])
except Exception as e:
    print("[!] Package installation failed:", e)

# ------------------------------
# 3. Download Vosk model (if missing)
# ------------------------------
if not os.path.exists(VOSK_DIR):
    print("[*] Downloading Vosk speech model...")
    url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    try:
        urllib.request.urlretrieve(url, VOSK_ZIP)
        with zipfile.ZipFile(VOSK_ZIP, "r") as zip_ref:
            zip_ref.extractall(MODELS_DIR)
        os.remove(VOSK_ZIP)
        print("[+] Vosk model ready at:", VOSK_DIR)
    except Exception as e:
        print("[!] Failed to fetch Vosk model:", e)
else:
    print("[*] Vosk model already present.")

# ------------------------------
# 4. Check BioMedLM presence
# ------------------------------
if not os.path.exists(BIO_MODEL_DIR):
    print("[!] BioMedLM model folder not found at:", BIO_MODEL_DIR)
    print("    Place the model files manually before running offline.")
    print("    Example structure:")
    print("    models/BioMedLM/config.json")
    print("    models/BioMedLM/pytorch_model.bin")
    print("    models/BioMedLM/tokenizer.json")
else:
    print("[+] BioMedLM model detected.")

# ------------------------------
# 5. Summary
# ------------------------------
print("\n Setup complete.")
print("Make sure BioMedLM is copied locally before going offline.")
print("Then run your main Medimind script normally.\n")
