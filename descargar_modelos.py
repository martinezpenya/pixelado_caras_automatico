import os
import urllib.request

BASE_URL = "https://github.com/lindevs/yolov8-face/releases/download/1.0.1/"
MODELS = [
    "yolov8n-face-lindevs.pt",
    "yolov8s-face-lindevs.pt",
    "yolov8m-face-lindevs.pt",
    "yolov8l-face-lindevs.pt",
    "yolov8x-face-lindevs.pt"
]

print("--- Descargando todos los modelos de caras / Downloading all face models ---")

for model in MODELS:
    if not os.path.exists(model):
        print(f"Descargando / Downloading: {model}...")
        urllib.request.urlretrieve(BASE_URL + model, model)
    else:
        print(f"Ya existe / Already exists: {model}")

print("¡Listo! / Done!")
