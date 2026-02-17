import tkinter as tk
from tkinter import scrolledtext
import cv2
import os
import datetime
import speech_recognition as sr
import pyttsx3
import requests
from googletrans import Translator
import face_recognition
import numpy as np

# ============ SETTINGS ============
OLLAMA_MODEL = "tinyllama"
ISSUE_FOLDER = "issues"
WORKER_FOLDER = "workers"
translator = Translator()

# Create folders
os.makedirs(ISSUE_FOLDER, exist_ok=True)
os.makedirs(WORKER_FOLDER, exist_ok=True)

# ============ VOICE ENGINE ============
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ============ SPEECH INPUT ============
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            return ""

# ============ LLM QUERY ============
def query_llm(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt}
        )
        return response.json()["response"]
    except:
        return "Model not available."

# ============ FACE FUNCTIONS ============
def register_worker():
    name = entry.get()
    if not name:
        return

    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()

    file_path = os.path.join(WORKER_FOLDER, f"{name}.jpg")
    cv2.imwrite(file_path, frame)

    chat.insert(tk.END, f"Worker {name} registered.\n")

def identify_worker():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()

    unknown_encoding = face_recognition.face_encodings(frame)
    if not unknown_encoding:
        return "Unknown"

    unknown_encoding = unknown_encoding[0]

    for file in os.listdir(WORKER_FOLDER):
        img = face_recognition.load_image_file(os.path.join(WORKER_FOLDER, file))
        known_encoding = face_recognition.face_encodings(img)[0]

        match = face_recognition.compare_faces([known_encoding], unknown_encoding)
        if match[0]:
            return file.split(".")[0]

    return "Unknown"

# ============ ISSUE CAPTURE ============
def capture_issue(worker):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(ISSUE_FOLDER, f"{worker}_{timestamp}.jpg")
    cv2.imwrite(file_path, frame)

# ============ MAIN ASK FUNCTION ============
def ask():
    user_text = entry.get()
    if not user_text:
        return

    worker = identify_worker()
    capture_issue(worker)

    # Detect language
    lang = translator.detect(user_text).lang

    translated = translator.translate(user_text, dest="en").text
    response = query_llm(translated)
    final_response = translator.translate(response, dest=lang).text

    chat.insert(tk.END, f"{worker}: {user_text}\n")
    chat.insert(tk.END, f"Bot: {final_response}\n\n")

    speak(final_response)
    entry.delete(0, tk.END)

# ============ VOICE BUTTON ============
def voice_input():
    text = listen()
    entry.insert(0, text)
    ask()

# ============ UI ============
root = tk.Tk()
root.title("Factory Assistant AI")

chat = scrolledtext.ScrolledText(root, width=60, height=20)
chat.pack()

entry = tk.Entry(root, width=50)
entry.pack()

ask_btn = tk.Button(root, text="Ask", command=ask)
ask_btn.pack()

voice_btn = tk.Button(root, text="🎤 Voice", command=voice_input)
voice_btn.pack()

reg_btn = tk.Button(root, text="Register Worker", command=register_worker)
reg_btn.pack()

status_label = tk.Label(root, text="Ready")
status_label.pack()

root.mainloop()
