# Instrucciones para Agentes IA

## Comandos Principales

### Backend

- `cd backend`
- `python run.py`

### Frontend

- `cd frontend`
- `npm install`
- `npm run dev`

### Tests

- Build: `npm run build`
- Tests: `pytest`
- Lint: `ruff check`

## Estilo de Código
- Usa black para formateo.
- Siempre añade tests.



## Límites
- Nunca modifiques archivos fuera de los siguientes directorios:
    - backend/
    - frontend/
    - android_app/
    - ios_app/
    - context/
    - AGENTS.md
    - README.md
    - .gitignore
    - .vscode/
- Pregunta antes de cambios mayores.
- Al finalizar tarea, actualiza context/04-tasks.md