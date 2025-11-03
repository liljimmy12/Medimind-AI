import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog
import sounddevice as sd
import queue
import vosk
import pyttsx3
import threading
import time
from model_interface import analyze_user_condition

# ------------------------------
# Paths
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "astronaut_data")
VOSK_MODEL_PATH = os.path.join(BASE_DIR, "models/vosk-model-small-en-us-0.15")

if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

# ------------------------------
# Voice Setup
# ------------------------------
q = queue.Queue()
vosk_model = vosk.Model(VOSK_MODEL_PATH)
engine = pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def voice_record(timeout_silence=5):
    """Record audio until silence timeout and return recognized text"""
    rec = vosk.KaldiRecognizer(vosk_model, 16000)
    last_speech_time = time.time()
    text = ""
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=lambda indata, frames, t, s: q.put(bytes(indata))):
        print("Listening for symptoms...")
        while True:
            try:
                data = q.get(timeout=0.1)
            except queue.Empty:
                data = None

            if data:
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    partial_text = result.get("text", "")
                    if partial_text.strip():
                        text += " " + partial_text
                        last_speech_time = time.time()
            # Check for silence timeout
            if time.time() - last_speech_time > timeout_silence and text.strip():
                break
    # Final result
    final_result = json.loads(rec.FinalResult())
    text += " " + final_result.get("text", "")
    return text.strip()

def listen_for_wake_word(wake_word="medimind start"):
    rec = vosk.KaldiRecognizer(vosk_model, 16000)
    print("Say the wake word to start the system...")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=lambda indata, frames, t, s: q.put(bytes(indata))):
        while True:
            try:
                data = q.get(timeout=0.1)
            except queue.Empty:
                continue
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").lower()
                if wake_word in text:
                    print("Wake word detected! Launching system...")
                    speak_text("System activated. Please describe your symptoms.")
                    return

# ------------------------------
# GUI App
# ------------------------------
class HealthGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🚀 Medimind-AI Emergency Health Monitor")
        self.geometry("600x500")
        self.configure(bg="#1a1a1a")
        self.create_widgets()

    def create_widgets(self):
        # Header
        tk.Label(self, text="Astronaut Health Emergency System", font=("Arial", 18, "bold"),
                 fg="#00ffcc", bg="#1a1a1a").pack(pady=10)

        # Name entry
        tk.Label(self, text="Enter astronaut name:", fg="white", bg="#1a1a1a").pack()
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.pack(pady=5)

        # Symptoms entry (manual override)
        tk.Label(self, text="Enter symptoms (comma-separated):", fg="white", bg="#1a1a1a").pack()
        self.symptoms_entry = tk.Entry(self, width=50)
        self.symptoms_entry.pack(pady=5)

        # Buttons
        tk.Button(self, text="🎤 Speak Symptoms Now", bg="#ffcc00", fg="black",
                  command=lambda: threading.Thread(target=self.voice_input).start()).pack(pady=10)
        tk.Button(self, text="Quick Emergency Vitals", bg="#ff4c4c", fg="white",
                  command=self.quick_emergency_input).pack(pady=5)
        tk.Button(self, text="Run AI Analysis", bg="#00ccff", fg="white",
                  command=lambda: threading.Thread(target=self.run_analysis).start()).pack(pady=10)

        # Output box
        self.output_text = tk.Text(self, height=15, width=70, bg="#333333", fg="#00ffcc")
        self.output_text.pack(pady=10)

    # ------------------------------
    # Functions
    # ------------------------------
    def voice_input(self):
        """Record symptoms with automatic 5s silence detection"""
        try:
            text = voice_record(timeout_silence=5)
            if text:
                self.symptoms_entry.delete(0, tk.END)
                self.symptoms_entry.insert(0, text)
                messagebox.showinfo("Voice Input Captured", f"Captured symptoms: {text}")
                self.run_analysis()
            else:
                messagebox.showwarning("No Input", "Could not capture symptoms.")
        except Exception as e:
            messagebox.showerror("Error", f"Voice input failed: {e}")

    def quick_emergency_input(self):
        """Prompt for emergency vitals"""
        self.vitals = {}
        try:
            self.vitals["heart_rate"] = simpledialog.askstring("Vitals", "Heart rate (bpm):")
            self.vitals["blood_pressure"] = simpledialog.askstring("Vitals", "Blood pressure (systolic/diastolic):")
            self.vitals["oxygen_saturation"] = simpledialog.askstring("Vitals", "Oxygen saturation (%):")
            self.vitals["body_temperature"] = simpledialog.askstring("Vitals", "Body temperature (°C):")
            self.vitals["respiratory_rate"] = simpledialog.askstring("Vitals", "Respiratory rate (breaths/min):")
            self.vitals["sleep_hours"] = simpledialog.askstring("Vitals", "Sleep hours (per day):")
            messagebox.showinfo("Vitals Recorded", "Emergency vitals saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to record vitals: {e}")

    def run_analysis(self):
        """Run AI analysis and display + speak results"""
        name = self.name_entry.get().strip().lower()
        symptoms = self.symptoms_entry.get().strip().lower().split(",")

        if not name or not symptoms:
            messagebox.showwarning("Input Required", "Please enter both name and symptoms.")
            return

        # Update JSON file
        user_file = os.path.join(DATA_PATH, f"{name}.json")
        if os.path.exists(user_file):
            with open(user_file, "r") as f:
                data = json.load(f)
        else:
            data = {"name": name, "vital_signs": {}, "recent_symptoms": []}

        # Update vitals if available
        if hasattr(self, "vitals"):
            data["vital_signs"].update(self.vitals)
        data["recent_symptoms"] = symptoms

        with open(user_file, "w") as f:
            json.dump(data, f, indent=4)

        # Capture AI output
        try:
            import io, sys
            buffer = io.StringIO()
            sys.stdout = buffer
            analyze_user_condition(DATA_PATH, name)
            sys.stdout = sys.__stdout__

            output = buffer.getvalue()
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, output)
            speak_text(output)
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {e}")

# ------------------------------
# Run voice-activated system
# ------------------------------
if __name__ == "__main__":
    # Start with wake word listening in main thread
    listen_for_wake_word("medimind start")
    app = HealthGUI()
    app.mainloop()