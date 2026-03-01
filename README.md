# 🛡️ Pixelado de caras automático / AI Face Anonymizer

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

<img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/es.svg" width="20"> **Castellano**  
Herramienta de alta seguridad para la protección de datos que detecta y destruye la información facial en fotos y vídeos de forma **totalmente irreversible**. Profesional, rápida y fácil de usar.

<img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/gb.svg" width="20"> **British English**  
High-security tool for data protection that detects and destroys facial information in photos and videos in a **completely irreversible** way. Professional, fast, and easy to use.

---

## ✨ Características / Features

<img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/es.svg" width="16"> **Seguridad Garantizada:** Pixelado mosaico destructivo e irreversible. Elimina físicamente la información original.  
<img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/gb.svg" width="16"> **Guaranteed Security:** Destructive mosaic pixelation. Physically removes original information.

<img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/es.svg" width="16"> **Multiformato:**  
- **Fotos:** `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`, `.tiff`, `.avif`, `.jfif`, etc.  
- **Vídeos:** `.mp4`, `.webm`, `.avi`, `.mov`, `.mkv`, `.mpeg`, `.wmv`, `.flv`, etc.  
<img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/gb.svg" width="16"> **Multiformat:** Supports all major photo and video formats.

<img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/es.svg" width="16"> **Precisión IA:** Basado en YOLOv8 con 5 tamaños de modelo.  
<img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/gb.svg" width="16"> **AI Precision:** Powered by YOLOv8 with 5 different model sizes.

---

## ⚙️ Configuración / Configuration (config.ini)

<img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/es.svg" width="16"> El archivo `config.ini` se crea solo la primera vez que arrancas el programa.  
<img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/gb.svg" width="16"> The `config.ini` file is created automatically on the first run.

- `model_size`: Selección del modelo / AI model selection (n, s, m, l, x).
- `blocks_across`: Resolución del pixelado (10 recomendado). / Number of blocks for pixelation.
- `box_padding`: Margen extra alrededor de la cara. / Margin around the face.
- `video_crf`: Calidad de compresión de vídeo. / Video compression quality.
- `min_confidence`: Sensibilidad de detección (0.0 a 1.0). / AI sensitivity.

---

## 🚀 Inicio Rápido / Quick Start

1. **Install Python:** [Python 3.10+](https://www.python.org/downloads/).
2. **Requirements / Requisitos:** 
   ```bash
   pip install -r requirements.txt
   ```
3. **Uso / Usage:** 
   - <img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/es.svg" width="16"> Pon tus archivos en la carpeta raíz. / <img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/gb.svg" width="16"> Place your files in the root folder.
   - Run: `python pixelado_caras_automatico.py`
   - <img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/es.svg" width="16"> Resultados en la carpeta `/anonymized`. / <img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/gb.svg" width="16"> Results in the `/anonymized` folder.

### 📦 Modelos Offline / Offline Models
<img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/es.svg" width="16"> Si quieres descargar todos los modelos de golpe:  
<img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/gb.svg" width="16"> To download all models at once for offline use:
```bash
python descargar_modelos.py
```

---

## ⚖️ Licencia / License
<img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/es.svg" width="16"> Este software se distribuye bajo la licencia **GNU Affero General Public License v3.0 (AGPL-3.0)**.  
<img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/gb.svg" width="16"> Licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

---

## 📝 Notas de Seguridad / Safety Notes
- <img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/es.svg" width="16"> El pixelado es de 12 bloques fijos, garantizando el anonimato.  
- <img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/gb.svg" width="16"> Fixed 12-block pixelation ensures consistent anonymity.
- <img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/es.svg" width="16"> El proceso es **destructivo**: los píxeles originales se eliminan.  
- <img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/gb.svg" width="16"> This process is **destructive**: original pixels are permanently deleted.
