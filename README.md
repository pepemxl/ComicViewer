# ComicViewer
A Comic Viewer




```bash
# backend
cd backend
python run.py    # http://localhost:8000

# frontend
cd frontend
npm install
npm run dev      # http://localhost:5173
```

```bash
comicviewer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── auth.py
│   │   └── utils.py
│   ├── comics/
│   ├── cache/
│   ├── requirements.txt
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── lib/api.ts
│   │   ├── routes/
│   │   │   ├── +page.svelte
│   │   │   └── comic/[id]/+page.svelte
│   │   └── app.html
│   ├── static/
│   │   ├── manifest.json
│   │   ├── sw.js                ← Service Worker PWA
│   │   ├── icon-192.png
│   │   ├── icon-512.png
│   │   └── favicon.png
│   ├── svelte.config.js
│   ├── vite.config.ts
│   └── package.json
│
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── Caddyfile
├── README.md
└── .gitignore
``