# ----------only chat app working here testing period  Voice (optional) ----------
import tkinter as tk
from tkinter import scrolledtext
import requests
import threading
import pyttsx3

MODEL = "phi3:mini"


# ---------- Voice (optional) ----------
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ---------- LLM ----------
def ask_llm(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]
    except:
        return "Model not responding. Is ollama running?"

# ---------- Ask Button ----------
def send_message():
    user_text = entry.get().strip()
    if not user_text:
        return

    chat_box.insert(tk.END, "You: " + user_text + "\n")
    entry.delete(0, tk.END)

    def process():
        reply = ask_llm(user_text)
        chat_box.insert(tk.END, "Bot: " + reply + "\n\n")
        speak(reply)

    threading.Thread(target=process).start()

# ---------- UI ----------
root = tk.Tk()
root.title("Offline Factory Chatbot")
root.geometry("600x500")

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD)
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

ask_button = tk.Button(root, text="Ask", command=send_message)
ask_button.pack(pady=5)

root.mainloop()
