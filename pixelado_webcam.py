# ==============================================================================
# Pixelado de caras en tiempo real - Webcam (AI Face Anonymizer - Live)
# Real-time face detection and anonymization using the system webcam.
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
import torch
import numpy as np
import sys
import configparser
import argparse
import time
import urllib.request
from pathlib import Path
from ultralytics import YOLO
from datetime import datetime

# --- CONFIGURACIÓN DE LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler("webcam_anonymizer.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# --- MODELOS DISPONIBLES ---
BASE_URL = "https://github.com/lindevs/yolov8-face/releases/download/1.0.1/"
MODELS = {
    "n": "yolov8n-face-lindevs.pt",  # Nano  - Ultra rápido
    "s": "yolov8s-face-lindevs.pt",  # Small - Rápido
    "m": "yolov8m-face-lindevs.pt",  # Medium - Equilibrado
    "l": "yolov8l-face-lindevs.pt",  # Large - Preciso
    "x": "yolov8x-face-lindevs.pt",  # Extra Large - Muy preciso
}

CONFIG_FILE = "config.ini"
CAPTURES_DIR = Path("./capturas")


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    elif '__compiled__' in globals():
        return os.path.join(os.path.dirname(sys.executable), relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)


def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        return config['SETTINGS']
    # Valores por defecto si no existe config.ini
    return {
        'model_size': 'n',
        'blocks_across': '10',
        'box_padding': '0.25',
        'min_confidence': '0.2',
        'img_size': '640',
    }


def ensure_model(model_filename, model_path):
    if not os.path.exists(model_path):
        url = BASE_URL + model_filename
        logger.info(f"Descargando modelo: {model_filename} ...")
        try:
            urllib.request.urlretrieve(url, model_path)
            logger.info("Descarga completada.")
        except Exception as e:
            logger.error(f"Error descargando el modelo: {e}")
            sys.exit(1)


def irreversible_pixelate(frame, box, blocks, padding):
    x1, y1, x2, y2 = map(int, box)
    w_box, h_box = x2 - x1, y2 - y1
    x1 = max(0, int(x1 - w_box * padding))
    y1 = max(0, int(y1 - h_box * padding))
    x2 = min(frame.shape[1], int(x2 + w_box * padding))
    y2 = min(frame.shape[0], int(y2 + h_box * padding))
    roi = frame[y1:y2, x1:x2]
    if roi.size == 0:
        return frame
    h, w = roi.shape[:2]
    small_w = blocks
    small_h = max(1, int(h * (blocks / w)))
    temp = cv2.resize(roi, (small_w, small_h), interpolation=cv2.INTER_AREA)
    pixelated = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
    frame[y1:y2, x1:x2] = pixelated
    return frame


def draw_overlay(frame, fps, pixelate_active, model_name, recording, num_faces):
    """Dibuja el HUD informativo sobre el frame."""
    h, w = frame.shape[:2]
    overlay = frame.copy()

    # Fondo semitransparente arriba
    cv2.rectangle(overlay, (0, 0), (w, 90), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    # FPS
    fps_color = (0, 255, 100) if fps >= 15 else (0, 165, 255) if fps >= 8 else (0, 0, 255)
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, fps_color, 2, cv2.LINE_AA)

    # Modelo
    cv2.putText(frame, f"Modelo: {model_name}", (10, 58),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (200, 200, 200), 1, cv2.LINE_AA)

    # Caras detectadas
    faces_color = (0, 255, 100) if num_faces > 0 else (150, 150, 150)
    cv2.putText(frame, f"Caras: {num_faces}", (10, 83),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, faces_color, 1, cv2.LINE_AA)

    # Estado pixelado
    pix_text = "PIXELADO: ON" if pixelate_active else "PIXELADO: OFF"
    pix_color = (0, 255, 100) if pixelate_active else (0, 100, 255)
    text_size = cv2.getTextSize(pix_text, cv2.FONT_HERSHEY_SIMPLEX, 0.75, 2)[0]
    cv2.putText(frame, pix_text, (w - text_size[0] - 10, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, pix_color, 2, cv2.LINE_AA)

    # REC indicator
    if recording:
        cv2.circle(frame, (w - 20, 60), 8, (0, 0, 255), -1)
        cv2.putText(frame, "REC", (w - 50, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)

    # Ayuda de teclas (abajo)
    help_bg = frame.copy()
    cv2.rectangle(help_bg, (0, h - 30), (w, h), (0, 0, 0), -1)
    cv2.addWeighted(help_bg, 0.5, frame, 0.5, 0, frame)
    keys_text = "ESPACIO: pixelado ON/OFF  |  S: captura  |  R: grabar  |  Q/ESC: salir"
    cv2.putText(frame, keys_text, (8, h - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1, cv2.LINE_AA)

    return frame


def parse_args():
    parser = argparse.ArgumentParser(
        description="Pixelado de caras en tiempo real usando la webcam."
    )
    parser.add_argument(
        "--webcam", type=int, default=0, metavar="N",
        help="Índice de la webcam a usar (por defecto: 0)"
    )
    parser.add_argument(
        "--model", choices=["n", "s", "m", "l", "x"], default=None,
        help="Tamaño del modelo YOLOv8 (n=rápido, x=preciso). Por defecto: valor de config.ini"
    )
    parser.add_argument(
        "--conf", type=float, default=None,
        help="Umbral de confianza para la detección (por defecto: valor de config.ini)"
    )
    parser.add_argument(
        "--no-gpu", action="store_true",
        help="Forzar uso de CPU aunque haya GPU disponible"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    settings = load_config()

    # --- Configuración ---
    m_size = args.model if args.model else settings.get('model_size', 'n').lower()
    if m_size not in MODELS:
        m_size = 'n'
    model_filename = MODELS[m_size]
    model_path = resource_path(model_filename)

    conf = args.conf if args.conf is not None else float(settings.get('min_confidence', 0.2))
    imgsz = int(settings.get('img_size', 640))
    blocks = int(settings.get('blocks_across', 10))
    padding = float(settings.get('box_padding', 0.25))
    device = 'cpu' if args.no_gpu else ('cuda' if torch.cuda.is_available() else 'cpu')

    print("=" * 70)
    print("      Pixelado de caras en tiempo real - Webcam (AI Face Anonymizer)")
    print("=" * 70)
    print(f"  Dispositivo : {device.upper()}")
    print(f"  Modelo      : {model_filename}")
    print(f"  Confianza   : {conf}")
    print(f"  Webcam      : {args.webcam}")
    print("=" * 70)
    print("  Controles:")
    print("    ESPACIO  → Activar / desactivar pixelado")
    print("    S        → Guardar captura de pantalla")
    print("    R        → Iniciar / parar grabación de vídeo")
    print("    Q / ESC  → Salir")
    print("=" * 70)

    # --- Cargar modelo ---
    ensure_model(model_filename, model_path)
    logger.info(f"Cargando modelo {model_filename} en {device.upper()}...")
    model = YOLO(model_path)
    model.to(device)
    logger.info("Modelo cargado.")

    # --- Abrir webcam ---
    cap = cv2.VideoCapture(args.webcam)
    if not cap.isOpened():
        logger.error(f"No se pudo abrir la webcam (índice {args.webcam}).")
        sys.exit(1)

    # Intentar configurar resolución razonable
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    cam_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cam_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cam_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    logger.info(f"Webcam abierta: {cam_w}x{cam_h} @ {cam_fps:.1f} fps")

    # --- Directorio de capturas ---
    CAPTURES_DIR.mkdir(parents=True, exist_ok=True)

    # --- Estado ---
    pixelate_active = True
    recording = False
    video_writer = None
    prev_time = time.time()
    fps = 0.0
    window_name = "Pixelado Webcam - AI Face Anonymizer"

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, cam_w, cam_h)

    logger.info("Iniciando captura. Pulsa Q o ESC para salir.")

    while True:
        ret, frame = cap.read()
        if not ret:
            logger.warning("No se pudo leer el frame de la webcam.")
            break

        # --- Detección ---
        num_faces = 0
        if pixelate_active:
            results = model.predict(frame, conf=conf, imgsz=imgsz, verbose=False)
            for result in results:
                if result.boxes is not None:
                    boxes = result.boxes.xyxy.cpu().numpy()
                    num_faces = len(boxes)
                    for box in boxes:
                        frame = irreversible_pixelate(frame, box, blocks, padding)

        # --- FPS ---
        current_time = time.time()
        elapsed = current_time - prev_time
        if elapsed > 0:
            fps = 0.9 * fps + 0.1 * (1.0 / elapsed)  # Media exponencial suavizada
        prev_time = current_time

        # --- HUD ---
        display_frame = draw_overlay(
            frame.copy(), fps, pixelate_active,
            model_filename, recording, num_faces
        )

        # --- Grabación ---
        if recording and video_writer is not None:
            video_writer.write(frame)  # Graba sin HUD para vídeo limpio

        # --- Mostrar ---
        cv2.imshow(window_name, display_frame)

        # --- Teclado ---
        key = cv2.waitKey(1) & 0xFF

        if key in (ord('q'), ord('Q'), 27):  # Q o ESC
            break

        elif key == ord(' '):  # ESPACIO - toggle pixelado
            pixelate_active = not pixelate_active
            estado = "activado" if pixelate_active else "desactivado"
            logger.info(f"Pixelado {estado}.")

        elif key in (ord('s'), ord('S')):  # S - captura
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            capture_path = CAPTURES_DIR / f"captura_{ts}.jpg"
            cv2.imwrite(str(capture_path), display_frame)
            logger.info(f"Captura guardada: {capture_path}")

        elif key in (ord('r'), ord('R')):  # R - grabar / parar
            if not recording:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                video_path = CAPTURES_DIR / f"grabacion_{ts}.mp4"
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                video_writer = cv2.VideoWriter(
                    str(video_path), fourcc, cam_fps, (cam_w, cam_h)
                )
                recording = True
                logger.info(f"Grabación iniciada: {video_path}")
            else:
                recording = False
                if video_writer:
                    video_writer.release()
                    video_writer = None
                logger.info("Grabación detenida.")

    # --- Limpieza ---
    if recording and video_writer:
        video_writer.release()
        logger.info("Grabación finalizada al salir.")

    cap.release()
    cv2.destroyAllWindows()
    logger.info("Webcam cerrada. Hasta pronto.")


if __name__ == "__main__":
    main()
