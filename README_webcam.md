# Pixelado de caras en tiempo real – Webcam

Script complementario a `pixelado_caras_automatico.py` que aplica el mismo pixelado de caras con IA directamente sobre la imagen de la webcam, en tiempo real.

---

## Requisitos

Los mismos que el proyecto principal (ver `requirements.txt`). No es necesario instalar nada adicional.

---

## Uso (Recomendado)

Para facilitar la instalación y ejecución, se incluye el script `activar_entorno_webcam.sh`. Este script crea automáticamente un entorno virtual aislado en `~/pixelado_webcam`, instala las dependencias y lanza la aplicación.

```bash
# Otorgar permisos de ejecución (solo la primera vez)
chmod +x activar_entorno_webcam.sh

# Opción A: Activar entorno y lanzar la aplicación automáticamente
./activar_entorno_webcam.sh

# Opción B: Activar el entorno en tu terminal (para uso manual)
source activar_entorno_webcam.sh
python pixelado_webcam.py
```

Al usar la **Opción A**, también puedes pasar las opciones de línea de comandos directamente al script:

```bash
./activar_entorno_webcam.sh --webcam 1 --model n --conf 0.3 --no-gpu
```

### Opciones disponibles

| Opción | Descripción | Por defecto |
|--------|-------------|-------------|
| `--webcam N` | Índice de la webcam a usar | `0` |
| `--model {n,s,m,l,x}` | Tamaño del modelo YOLOv8 | valor de `config.ini` |
| `--conf FLOAT` | Umbral de confianza para la detección | valor de `config.ini` |
| `--no-gpu` | Forzar CPU aunque haya GPU disponible | — |

> **Consejo:** Para uso en webcam se recomienda `--model n` (Nano) o `--model s` (Small) para obtener una tasa de frames fluida. El modelo `x` (Extra Large, predeterminado en `config.ini`) puede resultar lento en tiempo real.

---

## Controles durante la ejecución

| Tecla | Acción |
|-------|--------|
| `ESPACIO` | Activar / desactivar el pixelado |
| `S` | Guardar captura de pantalla en `./capturas/` |
| `R` | Iniciar / parar grabación de vídeo en `./capturas/` |
| `Q` / `ESC` | Salir |

---

## HUD (información en pantalla)

- **FPS en tiempo real** — verde (≥15 fps), naranja (≥8 fps), rojo (<8 fps)
- **Modelo activo** y **número de caras** detectadas en el frame actual
- **Estado del pixelado** — ON (verde) / OFF (naranja)
- **Indicador REC** — círculo rojo visible mientras se graba
- **Barra de ayuda** con los controles en la parte inferior de la imagen

---

## Salida generada

Las capturas y grabaciones se guardan automáticamente en la carpeta `./capturas/` (se crea si no existe):

| Fichero | Descripción |
|---------|-------------|
| `capturas/captura_YYYYMMDD_HHMMSS.jpg` | Captura de pantalla (con HUD) |
| `capturas/grabacion_YYYYMMDD_HHMMSS.mp4` | Grabación de vídeo (sin HUD, imagen limpia) |

Los eventos también quedan registrados en `webcam_anonymizer.log`.

---

## Relación con el proyecto principal

`pixelado_webcam.py` reutiliza:
- El mismo modelo YOLOv8 (`yolov8*-face-lindevs.pt`) y la configuración de `config.ini`.
- La misma lógica de pixelado irreversible.

No modifica ningún archivo del proyecto original.
