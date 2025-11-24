# Variables
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
REQUIREMENTS = requirements.txt

# Objetivo principal (por defecto ejecuta `make install`)
all: install

# Crear entorno virtual e instalar dependencias
install:
	@echo "Creando entorno virtual..."
	python3 -m venv $(VENV)
	@echo "Instalando dependencias..."
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS)
	@echo "\n✅ Entorno listo. Actívalo con: source $(VENV)/bin/activate"

# Ejecutar el visualizador
run:
	$(PYTHON) comic_viewer.py

# Limpiar entorno virtual
clean:
	@echo "Eliminando entorno virtual..."
	rm -rf $(VENV)
	@echo "Entorno eliminado."

# Ayuda
help:
	@echo "Opciones disponibles:"
	@echo "  make install   - Crea el entorno virtual e instala dependencias."
	@echo "  make run       - Ejecuta el visualizador (con el entorno activado)."
	@echo "  make clean     - Elimina el entorno virtual."
	@echo "  make help      - Muestra esta ayuda."

.PHONY: all install run clean help