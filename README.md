🖥 STEP 1 — Update Raspberry Pi

Open terminal:

sudo apt update
sudo apt upgrade -y

🐍 STEP 2 — Install Python & Tools
sudo apt install python3 python3-pip python3-venv -y


Check version:

python3 --version

🎥 STEP 3 — Install Camera Dependencies
sudo apt install libatlas-base-dev libjasper-dev libqtgui4 libqt4-test -y
sudo apt install python3-opencv -y


Test camera:

python3


Inside Python:

import cv2
cam = cv2.VideoCapture(0)
print(cam.read())


If it prints True → camera works.

🎤 STEP 4 — Install Voice Packages (Offline)
sudo apt install espeak -y
pip3 install pyttsx3
pip3 install SpeechRecognition
sudo apt install python3-pyaudio -y


For offline recognition (Sphinx):

pip3 install pocketsphinx


⚠️ If this fails on Pi, skip offline speech — Pi sometimes struggles compiling it.

🖼 STEP 5 — Install Pillow
pip3 install pillow


Needed for:

from PIL import Image, ImageTk

🌐 STEP 6 — Install Requests (for Ollama)
pip3 install requests

🧠 STEP 7 — Install Ollama (Optional AI Model)

If you want offline LLM:

curl -fsSL https://ollama.com/install.sh | sh


Start ollama:

ollama serve


Open new terminal:

Install lightweight model:

ollama pull phi3:mini


OR smaller:

ollama pull tinyllama


Test:

ollama run phi3:mini


If it responds → working.

🌎 STEP 8 — Install Google Translate (Online Only)
pip3 install googletrans==4.0.0-rc1


⚠️ Needs internet.

👤 STEP 9 — Install Face Recognition (VERY HEAVY)

⚠️ On Raspberry Pi this is difficult.

Install dependencies:

sudo apt install cmake
sudo apt install libopenblas-dev liblapack-dev
sudo apt install libjpeg-dev


Then:

pip3 install dlib
pip3 install face_recognition


⚠️ This can take 30–60 minutes and may fail.

If it fails:
👉 I recommend NOT using face recognition on Pi.

📂 STEP 10 — Project Folder Setup

Create project folder:

mkdir factory_ai
cd factory_ai


Save your main code as:

nano app.py


Paste code → Save:
CTRL + X
Press Y
Press Enter

▶️ STEP 11 — Run Program
python3 app.py

🖥 STEP 12 — Run in Fullscreen Kiosk Mode

Add this to top of your UI:

root.attributes("-fullscreen", True)


Exit with:
ESC key

🚀 STEP 13 — Auto Start on Boot (Startup Service)

Create service:

sudo nano /etc/systemd/system/factory.service


Paste:

[Unit]
Description=Factory AI
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/factory_ai/app.py
WorkingDirectory=/home/pi/factory_ai
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target


Save.

Enable:

sudo systemctl daemon-reload
sudo systemctl enable factory.service
sudo systemctl start factory.service


Reboot test:

sudo reboot

🧯 If Program Freezes

Check CPU:

htop


If 100% → too heavy.

Fix:

Lower camera resolution

Remove face recognition

Remove google translate

Remove threads

💾 Storage Recommendation for Pi

✔ Use only:

tkinter

opencv

pillow

pyttsx3

simple smart_response

❌ Avoid:

dlib

face_recognition

heavy LLM models

multiple threads

🏆 BEST STABLE PI COMBINATION

For smooth Pi:

✔ Offline Smart Engine
✔ Camera capture
✔ Industrial UI
✔ Touch friendly buttons
✔ Emergency alert
✔ Worker ID manual entry
✔ No heavy AI
