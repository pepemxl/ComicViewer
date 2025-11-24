# Usa una imagen base con Python y soporte para GUI
FROM python:3.11-slim

# Instala dependencias del sistema (incluyendo libGL y herramientas para .cbz/.cbr)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    unrar \
    && rm -rf /var/lib/apt/lists/*

# Crea y activa el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt .
COPY comic_viewer.py .

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Permite mostrar la GUI en el host (Linux)
ENV DISPLAY=:0
ENV QT_X11_NO_MITSHM=1

# Comando por defecto al ejecutar el contenedor
CMD ["python", "comic_viewer.py"]