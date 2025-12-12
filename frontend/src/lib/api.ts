//const API_URL = "http://localhost:8000";

const API_URL = "/api";

export async function uploadComic(file: File) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_URL}/upload`, {
    method: "POST",
    body: form
  });
  return res.json();
}

export async function getComics() {
  const res = await fetch(`${API_URL}/comics`);
  return res.json();
}

export async function getComicPages(comicId: number) {
  const res = await fetch(`${API_URL}/comics/${comicId}/pages`);
  return res.json();
}

export function getPageUrl(comicId: number, pageIndex: number) {
  return `${API_URL}/comics/${comicId}/page/${pageIndex}`;
}

export let token = "";

export function setToken(t: string) {
  token = t;
  localStorage.setItem("token", t);
}

if (typeof window !== "undefined") {
  token = localStorage.getItem("token") || "";
}

// Todas las fetch ahora incluyen el token
// Usa authFetch en lugar de fetch en todas las funciones
async function authFetch(url: string, options: RequestInit = {}) {
  const headers = new Headers(options.headers || {});
  if (token) headers.set("AuthorizationAko", `Bearer ${token}`);
  return fetch(url, { ...options, headers });
}

