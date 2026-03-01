# 🛡️ Pixelado de caras automático (AI Face Anonymizer)

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

🇺🇸 High-security tool for data protection that detects and destroys facial information in photos and videos in a **completely irreversible** way. Professional, fast, and easy to use.

🇪🇸 Herramienta de alta seguridad para la protección de datos que detecta y destruye la información facial en fotos y vídeos de forma **totalmente irreversible**. Profesional, rápida y fácil de usar.

---

## ✨ Features / Características
- **Guaranteed Security / Seguridad Garantizada:** Destructive mosaic pixelation. Physically removes original information. / Pixelado mosaico destructivo e irreversible.
- **Multiformat / Multiformato:** 
  - **Photos:** `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`, `.tiff`, `.avif`, `.jfif`, etc.
  - **Videos:** `.mp4`, `.webm`, `.avi`, `.mov`, `.mkv`, `.mpeg`, `.wmv`, `.flv`, etc.
- **AI Precision / Precisión IA:** Powered by YOLOv8 with 5 different model sizes. / Basado en YOLOv8 con 5 tamaños de modelo.
- **Audio Preservation / Audio:** Keeps original audio track using FFmpeg. / Mantiene el audio original con FFmpeg.
- **Bilingual / Bilingüe:** Interface and logs in English & Castellano.

---

## ⚙️ Configuration / Configuración (config.ini)
🇺🇸 The `config.ini` file is created automatically on the first run.
🇪🇸 El archivo `config.ini` se crea solo la primera vez que arrancas el programa.

- `model_size`: AI model selection / Selección del modelo:
  - `n`: **Nano** (Ultra Fast / El más rápido)
  - `s`: **Small** (Fast / Rápido)
  - `m`: **Medium** (Balanced / Equilibrado)
  - `l`: **Large** (Accurate / Preciso)
  - `x`: **Extra Large** (Maximum Precision / Máxima precisión) - **Default**
- `blocks_across`: Number of blocks for pixelation (10 is recommended for strong anonymity). / Resolución del pixelado (10 recomendado para mayor seguridad).
- `box_padding`: Margin around the face (0.25 = 25% extra). / Margen extra alrededor de la cara.
- `video_crf`: Video quality (18 = high, 23 = medium, 28 = low). / Calidad de compresión.
- `min_confidence`: AI sensitivity (0.0 to 1.0). / Sensibilidad de detección.

---

## 🚀 Quick Start / Inicio Rápido

1. **Install Python:** [Python 3.10+](https://www.python.org/downloads/).
2. **Requirements / Requisitos:** 
   ```bash
   pip install -r requirements.txt
   ```
3. **Usage / Uso:** 
   - Place your files in the program folder. / Pon tus archivos en la carpeta.
   - Run: `python pixelado_caras_automatico.py`
   - Results will be in the `/anonymized` folder. / Resultados en la carpeta `/anonymized`.

### 📦 Offline Models / Modelos Offline
🇺🇸 If you want to download all models at once for offline use or redistribution:
🇪🇸 Si quieres descargar todos los modelos de golpe para usarlos sin internet o distribuirlos:
```bash
python descargar_modelos.py
```

---

## ⚖️ License / Licencia
🇺🇸 Licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.
🇪🇸 Este software se distribuye bajo la licencia **GNU Affero General Public License v3.0 (AGPL-3.0)**.

---

## 📝 Safety Notes / Notas de Seguridad
- The pixelation is **fixed at 12 blocks**, ensuring consistent anonymity regardless of image resolution. / El pixelado es de 12 bloques fijos, garantizando el anonimato sin importar la resolución.
- This process is **destructive**: original pixels are deleted and cannot be recovered. / El proceso es destructivo: los píxeles originales se eliminan y no pueden recuperarse.
