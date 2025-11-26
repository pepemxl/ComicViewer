<script lang="ts">
  import { page } from "$app/stores";
  import { getComicPages, getPageUrl } from "$lib/api";
  import { onMount } from "svelte";

  const comicId = $page.params.id;
  let pages: string[] = [];
  let current = 0;

  async function loadPages() {
    const data = await getComicPages(comicId);
    pages = data.pages;
  }

  function next() { if (current < pages.length - 1) current++; }
  function prev() { if (current > 0) current--; }

  // Teclas ← → y A D
  function handleKey(e: KeyboardEvent) {
    if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") next();
    if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") prev();
  }

  onMount(() => {
    loadPages();
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  });
</script>

<div class="fixed inset-0 bg-black text-white flex flex-col">
  <!-- Barra superior -->
  <div class="bg-gray-900 p-4 flex justify-between items-center z-10">
    <a href="/" class="hover:text-gray-300">Biblioteca</a>
    <div class="text-lg">
      Página {current + 1} / {pages.length}
    </div>
  </div>

  <!-- Imagen central -->
  <div class="flex-1 flex items-center justify-center overflow-hidden" on:click={next}>
    {#if pages.length > 0}
      <img 
        src={getPageUrl(comicId, current)} 
        alt="page {current}"
        class="max-w-full max-h-full object-contain"
      />

      <!-- Botones laterales grandes (móvil) -->
      <button on:click|stopPropagation={prev} class="absolute left-4 top-1/2 -translate-y-1/2 text-6xl opacity-30 hover:opacity-80">
        ←
      </button>
      <button on:click|stopPropagation={next} class="absolute right-4 top-1/2 -translate-y-1/2 text-6xl opacity-30 hover:opacity-80">
        →
      </button>
    {:else}
      <p class="text-2xl">Cargando páginas...</p>
    {/if}
  </div>
</div>