# Plan de Trabajo

## Fases del Proyecto
Plan de trabajo completo, realista y detallado para que una IA (o un equipo pequeño) construya un lector web de cómics CBZ/CBR ultra fluido:

**Tecnología elegida (la más usada y potente hoy):**
- Backend: **FastAPI** (Python 3.11+)
- Frontend: **SvelteKit**
- Base de datos: SQLite (dev) → PostgreSQL (producción)
- Autenticación: JWT
- Despliegue: Docker + Docker Compose → Fly.io / Render / Railway / Hetzner

### Plan de trabajo dividido en 8 sprints (2–10 semanas según velocidad)

#### Sprint 0 – Preparación (1–2 días)
- Crear repositorio Git (monorepo con backend/ y frontend/)
- Estructura inicial:
  ```
  comic-reader/
  ├── backend/          → FastAPI
  ├── frontend/         → SvelteKit (o React+Vite)
  ├── docker-compose.yml
  └── README.md
  ```
- Instalar dependencias básicas
- Configurar pre-commit (ruff, black, prettier)

#### Sprint 1 – Backend básico + lectura de CBZ (3–5 días)
Objetivo: Poder subir o seleccionar un .cbz y ver sus páginas como imágenes

Tareas para la IA:
1. Crear modelo `Comic` (id, título, ruta archivo, portada, número de páginas, fecha añadido)
2. Endpoint `/upload` → aceptar .cbz/.cbr y guardarlo en `./comics/`
3. Endpoint `/comics` → listar todos los cómics con metadata
4. Endpoint `/comics/{comic_id}/pages` → devolver lista de nombres de archivos dentro del ZIP (ordenados)
5. Endpoint `/comics/{comic_id}/page/{page_number}` → extraer y devolver la imagen en streaming (sin guardar en disco)
   - Usar `zipfile` (cbz) y `rarfile` + `unrar` (cbr)
   - Cachear páginas más vistas con `cachetools` o Redis (opcional después)
6. Extraer portada automática (primer archivo de imagen)

#### Sprint 2 – Frontend básico (SvelteKit recomendado) (4–6 días)
Objetivo: Ver la biblioteca y abrir un cómic

Tareas:
1. Página principal: grid de portadas (como Komga/Kavita)
2. Página de cómic: visor full-screen
3. Visor simple que:
   - Cargue página actual con `<img src="/api/comics/123/page/5">`
   - Botones anterior/siguiente
   - Teclas ← →, A D, espacio
   - Indicador de página actual / total
4. Responsive (móvil + desktop)

#### Sprint 3 – Visor profesional (el corazón del lector) (5–8 días)
Objetivo: Experiencia de lectura comparable a Tachiyomi/Mihon

Implementar en el frontend:
- Modos de lectura:
  - Página simple
  - Doble página (para cómics occidentales)
  - Webtoon (scroll vertical infinito)
- Dirección: L→R (manga) y R→L (cómics USA)
- Zoom con pinch y doble click
- Precarga inteligente de ±3 páginas
- Barra lateral o inferior con thumbnails de todas las páginas
- Guardar progreso de lectura por cómic y usuario
- Fullscreen real (F11 y botón)
- Modo oscuro/claro automático
- Soporte para gestos en móvil

Librería recomendada: usar componente propio (es más rápido y ligero que PhotoSwipe para cómics). Hay templates abiertos en GitHub 2025 que la IA puede copiar y mejorar.

#### Sprint 4 – Organización y metadata (4–6 días)
- Escanear carpeta automáticamente (`/comics` o volumen Docker)
- Soporte para estructura de carpetas:
  ```
  /comics/
    ├── One Piece/
    │   ├── One Piece v01.cbz
    │   └── One Piece v02.cbz
    ├── Batman/
    └── ...
  ```
- Agrupar por series
- Extraer metadata automática con ComicTagger / ComicVine API (opcional pero muy deseado)
- Búsqueda y filtros (por serie, leído/no leído, favorito)

#### Sprint 5 – Autenticación y multiusuario (3–5 días)
- Registro / login (email + password o OAuth Google/GitHub)
- Cada usuario tiene su propio progreso de lectura
- Opcional: modo “invitado” sin login

#### Sprint 6 – Optimizaciones de rendimiento (4–7 días)
- Convertir páginas a WebP en tiempo real (solo la primera vez) y cachear en `./cache/`
- Usar Redis o SQLite para cache de páginas extraídas
- Headers de cache correctos (ETag, Cache-Control)
- Compresión brotli/gzip
- Lazy load + IntersectionObserver

#### Sprint 7 – Características avanzadas (nice-to-have) (5–10 días)
- OPDS feed (para conectar con apps como Panels, Chunky, etc.)
- Descarga de cómic completo como ZIP
- Marcadores / favoritos
- Estadísticas de lectura
- Tema personalizado
- PWA (instalable en móvil)

#### Sprint 8 – Despliegue y polish final (3–5 días)
- Dockerizar todo (multi-stage builds)
- Variables de entorno (.env)
- HTTPS con Traefik o Caddy (o usar Fly.io que lo da gratis)
- Backup automático de la base de datos
- Dominio + Cloudflare

### Tiempo estimado total (trabajando una IA full-time)
- Versión mínima funcional (Sprints 1–3): 10–14 días
- Versión excelente (hasta Sprint 6): 4–6 semanas
- Versión casi perfecta (todo): 8–10 semanas

### Comando para que la IA

```bash
# Crear el proyecto (la IA puede ejecutar esto)
npx degit sveltejs/kit-template-default frontend
cd frontend && npm install
cd ../backend
poetry new backend && cd backend
poetry add fastapi uvicorn python-multipart python-rarfile unrar sqlite sqlalchemy
```


## Timeline Estimado
- Inicio: 21/01/2026
- Entrega MVP: 11/02/2026

## Riesgos
- Dependencias de base de datos.
- Mitigación: Usar variables de entorno.