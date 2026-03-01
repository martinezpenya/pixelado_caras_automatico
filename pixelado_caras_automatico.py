# ==============================================================================
# Pixelado de caras automático (AI Face Anonymizer)
# Professional tool for face detection and anonymization.
# Copyright (C) 2026
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ==============================================================================

import os
import cv2
import logging
import subprocess
import torch
import numpy as np
from pathlib import Path
from ultralytics import YOLO
from tqdm import tqdm
import urllib.request
import sys
import configparser

# --- CONFIGURACIÓN DE LOGGING / LOGGING CONFIG ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler("anonymizer.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# --- MODELOS DISPONIBLES / AVAILABLE MODELS ---
BASE_URL = "https://github.com/lindevs/yolov8-face/releases/download/1.0.1/"
MODELS = {
    "n": "yolov8n-face-lindevs.pt", # Nano - Ultra Fast
    "s": "yolov8s-face-lindevs.pt", # Small - Fast
    "m": "yolov8m-face-lindevs.pt", # Medium - Balanced
    "l": "yolov8l-face-lindevs.pt", # Large - Accurate
    "x": "yolov8x-face-lindevs.pt"  # Extra Large - Very Accurate (Slow but powerful)
}

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    elif '__compiled__' in globals():
        return os.path.join(os.path.dirname(sys.executable), relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)

def get_unique_path(path):
    if not path.exists(): return path
    stem, suffix, directory, counter = path.stem, path.suffix, path.parent, 1
    while True:
        new_path = directory / f"{stem}_{counter}{suffix}"
        if not new_path.exists(): return new_path
        counter += 1

# --- GESTIÓN DE CONFIGURACIÓN / CONFIG MANAGEMENT ---
CONFIG_FILE = "config.ini"

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        config['SETTINGS'] = {
            'model_size': 'x', # Cambiado a Extra Large por defecto / Default: X
            'blocks_across': '10',
            'box_padding': '0.25',
            'video_crf': '23',
            'min_confidence': '0.2',
            'img_size': '1280'
        }
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
    else:
        config.read(CONFIG_FILE)
    return config['SETTINGS']

# --- CONSTANTES / CONSTANTS ---
OUTPUT_DIR = Path("./anonymized")
VIDEO_EXTS = ('.mp4', '.webm', '.avi', '.mov', '.mkv', '.mpeg', '.mpg', '.m4v', '.3gp', '.wmv', '.flv')
IMAGE_EXTS = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff', '.tif', '.jfif', '.pjpeg', '.pjp', '.avif')

class FaceAnonymizer:
    def __init__(self, use_gpu=True):
        self.settings = load_config()
        self.device = 'cuda' if use_gpu and torch.cuda.is_available() else 'cpu'
        
        m_size = self.settings.get('model_size', 'x').lower()
        if m_size not in MODELS: m_size = 'x'
        self.model_filename = MODELS[m_size]
        self.model_path = resource_path(self.model_filename)
        
        logger.info(f"Device / Dispositivo: {self.device.upper()}")
        logger.info(f"Model / Modelo: {self.model_filename} (Size: {m_size})")
        
        self._ensure_model()
        self.model = YOLO(self.model_path)
        self.model.to(self.device)

    def _ensure_model(self):
        if not os.path.exists(self.model_path):
            url = BASE_URL + self.model_filename
            logger.info(f"Downloading model... / Descargando modelo: {self.model_filename}")
            try:
                urllib.request.urlretrieve(url, self.model_path)
                logger.info("Download complete. / Descarga completada.")
            except Exception as e:
                logger.error(f"Error downloading model: {e}")
                sys.exit(1)

    def irreversible_pixelate(self, frame, box):
        blocks = int(self.settings.get('blocks_across', 10))
        padding = float(self.settings.get('box_padding', 0.25))
        x1, y1, x2, y2 = map(int, box)
        w_box, h_box = x2 - x1, y2 - y1
        x1, y1 = max(0, int(x1 - w_box * padding)), max(0, int(y1 - h_box * padding))
        x2, y2 = min(frame.shape[1], int(x2 + w_box * padding)), min(frame.shape[0], int(y2 + h_box * padding))
        roi = frame[y1:y2, x1:x2]
        if roi.size == 0: return frame
        h, w = roi.shape[:2]
        small_w = blocks
        small_h = max(1, int(h * (blocks / w)))
        temp = cv2.resize(roi, (small_w, small_h), interpolation=cv2.INTER_AREA)
        pixelated = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
        frame[y1:y2, x1:x2] = pixelated
        return frame

    def process_image(self, input_path):
        conf = float(self.settings.get('min_confidence', 0.2))
        imgsz = int(self.settings.get('img_size', 1280))
        input_path = Path(input_path)
        output_path = get_unique_path(OUTPUT_DIR / input_path.name)
        img = cv2.imread(str(input_path))
        if img is None: return
        results = self.model.predict(img, conf=conf, imgsz=imgsz, verbose=False)
        for result in results:
            if result.boxes is not None:
                for box in result.boxes.xyxy.cpu().numpy():
                    img = self.irreversible_pixelate(img, box)
        cv2.imwrite(str(output_path), img)
        logger.info(f"DONE / FIN: {output_path.name}")

    def process_video(self, input_path):
        conf = float(self.settings.get('min_confidence', 0.2))
        imgsz = int(self.settings.get('img_size', 1280))
        input_path = Path(input_path)
        output_path = get_unique_path(OUTPUT_DIR / input_path.name)
        temp_output = OUTPUT_DIR / f"temp_{input_path.name}"
        cap = cv2.VideoCapture(str(input_path))
        if not cap.isOpened(): return
        fps = cap.get(cv2.CAP_PROP_FPS)
        width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(temp_output), fourcc, fps, (width, height))
        try:
            results = self.model.track(source=str(input_path), stream=True, persist=True, conf=conf, imgsz=imgsz, verbose=False)
            desc = f"Processing / Procesando: {input_path.name}"
            with tqdm(total=total_frames, desc=desc, ascii=True) as pbar:
                for result in results:
                    frame = result.orig_img.copy()
                    if result.boxes is not None:
                        for box in result.boxes.xyxy.cpu().numpy():
                            frame = self.irreversible_pixelate(frame, box)
                    out.write(frame)
                    pbar.update(1)
        finally:
            cap.release()
            out.release()
        self._reencode_with_ffmpeg(input_path, temp_output, output_path)
        if temp_output.exists(): temp_output.unlink()

    def _reencode_with_ffmpeg(self, original_path, processed_path, final_path):
        crf = self.settings.get('video_crf', '23')
        ffmpeg_cmd = './ffmpeg.exe' if os.path.exists('ffmpeg.exe') else 'ffmpeg'
        command = [
            ffmpeg_cmd, '-y', '-i', str(processed_path), '-i', str(original_path),
            '-map', '0:v:0', '-map', '1:a:0?', '-c:v', 'libx264', '-crf', crf,
            '-preset', 'medium', '-c:a', 'aac', '-shortest', str(final_path)
        ]
        try:
            subprocess.run(command, check=True, capture_output=True)
            logger.info(f"DONE / FIN: {final_path.name}")
        except:
            processed_path.rename(final_path)

def main():
    print("================================================================================")
    print("                Pixelado de caras automatico (AI Face Anonymizer)               ")
    print("================================================================================")
    print("[Castellano] Este programa usa IA para detectar y pixelar caras.")
    print("             Configuracion: Edita 'config.ini' para cambiar el modelo.")
    print("             Modelos: n, s, m, l, x (maxima precision - PREDETERMINADO).")
    print("================================================================================")
    print("")

    if not OUTPUT_DIR.exists(): OUTPUT_DIR.mkdir(parents=True)
    files = [f for f in os.listdir('.') if f.lower().endswith(VIDEO_EXTS + IMAGE_EXTS)]
    
    if not files:
        print(" [!] No compatible files found / No se han encontrado archivos compatibles.")
        print("")
        print(" [Castellano] INSTRUCCIONES:")
        print(" 1. Copia tus videos o fotos aqui.")
        print(" 2. Edita 'model_size' en 'config.ini' si quieres cambiar la velocidad/calidad.")
        print(" 3. Vuelve a ejecutar este programa.")
        print("")
        print(" [English] INSTRUCTIONS:")
        print(" 1. Copy your videos or photos here.")
        print(" 2. Edit 'model_size' in 'config.ini' to change speed vs quality.")
        print(" 3. Run this program again.")
        print("================================================================================")
        return

    anonymizer = FaceAnonymizer()
    for file in files:
        if file.lower().endswith(IMAGE_EXTS): anonymizer.process_image(file)
        else: anonymizer.process_video(file)

if __name__ == "__main__":
    main()
