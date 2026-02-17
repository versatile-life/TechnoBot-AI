import tkinter as tk
from tkinter import scrolledtext
import cv2
import os
import datetime
import speech_recognition as sr
import pyttsx3
from PIL import Image, ImageTk

# ================= SETTINGS =================
ISSUE_FOLDER = "issues"
os.makedirs(ISSUE_FOLDER, exist_ok=True)

# ================= VOICE ENGINE =================
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ================= SIMPLE SMART ENGINE =================
def smart_response(text):
    text = text.lower()

    if "overheat" in text or "hot" in text:
        return "Please check the coolant system and reduce machine load."

    elif "belt" in text:
        return "Inspect the conveyor belt for wear or misalignment."

    elif "not working" in text:
        return "Please restart the machine and check power connections."

    elif "noise" in text:
        return "Check motor bearings and lubrication."

    elif "help" in text:
        return "Please describe the machine issue clearly."

    else:
        return "Issue recorded. Technician will inspect shortly."

# ================= CAMERA =================
def update_camera():
    ret, frame = cam.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)
    camera_label.after(10, update_camera)

def capture_issue():
    ret, frame = cam.read()
    if ret:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(ISSUE_FOLDER, f"issue_{timestamp}.jpg")
        cv2.imwrite(file_path, frame)
        status_label.config(text=f"Issue Captured: {file_path}")

# ================= SPEECH INPUT (Offline) =================
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        audio = r.listen(source)

        try:
            text = r.recognize_sphinx(audio)  # OFFLINE recognition
            return text
        except:
            return ""

def voice_input():
    text = listen()
    entry.insert(0, text)
    ask()

# ================= ASK FUNCTION =================
def ask():
    user_text = entry.get()
    if not user_text:
        return

    response = smart_response(user_text)

    chat.insert(tk.END, f"You: {user_text}\n")
    chat.insert(tk.END, f"Bot: {response}\n\n")

    speak(response)
    entry.delete(0, tk.END)
    status_label.config(text="Ready")

# ================= UI =================
root = tk.Tk()
root.title("🏭 Factory Assistant AI - Raspberry Pi")
root.geometry("800x700")

# Camera
cam = cv2.VideoCapture(0)
camera_label = tk.Label(root)
camera_label.pack(pady=5)

capture_btn = tk.Button(root, text="📷 Capture Issue", command=capture_issue)
capture_btn.pack(pady=5)

# Chat
chat = scrolledtext.ScrolledText(root, width=90, height=15)
chat.pack(pady=10)

# Language Dropdown (UI only)
languages = [
    "English",
    "Hindi",
    "Tamil",
    "Telugu",
    "Kannada",
    "Marathi",
    "Bengali",
    "Gujarati"
]

language_var = tk.StringVar(value="English")
language_menu = tk.OptionMenu(root, language_var, *languages)
language_menu.pack(pady=5)

# Entry
entry = tk.Entry(root, width=70)
entry.pack(pady=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack()

ask_btn = tk.Button(button_frame, text="Ask", width=15, command=ask)
ask_btn.grid(row=0, column=0, padx=5)

voice_btn = tk.Button(button_frame, text="🎤 Speak", width=15, command=voice_input)
voice_btn.grid(row=0, column=1, padx=5)

status_label = tk.Label(root, text="Ready")
status_label.pack(pady=5)

update_camera()
root.mainloop()
