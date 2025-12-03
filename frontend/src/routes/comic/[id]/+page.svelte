<script lang="ts">
  import { page } from "$app/stores";
  import { getComicPages, getPageUrl } from "$lib/api";
  import { onMount, onDestroy } from "svelte";

  const comicId = $page.params.id;
  let pages: string[] = [];
  let current = 0;
  let readingDirection = "ltr";       // ltr = occidental, rtl = manga
  let readingMode = "double";         // single | double | webtoon
  let showSidebar = true;
  let isFullscreen = false;

  // Precarga
  const preloadCache = new Map<number, string>();

  async function loadPages() {
    const data = await getComicPages(comicId);
    pages = data.pages;
    preloadPagesAround(current);
  }

  function preloadPagesAround(center: number) {
    const range = 4;
    for (let i = Math.max(0, center - range); i < Math.min(pages.length, center + range + 4); i++) {
      if (!preloadCache.has(i)) {
        const img = new Image();
        img.src = getPageUrl(comicId, i);
        preloadCache.set(i, img.src);
      }
    }
  }

  function goTo(page: number) {
    current = Math.max(0, Math.min(pages.length - 1, page));
    preloadPagesAround(current);
    saveProgress();
  }

  function next() {
    if (readingMode === "webtoon") {
      window.scrollBy({ top: window.innerHeight * 0.9, behavior: "smooth" });
      return;
    }
    const increment = readingMode === "double" ? 2 : 1;
    goTo(current + increment);
  }

  function prev() {
    if (readingMode === "webtoon") {
      window.scrollBy({ top: -window.innerHeight * 0.9, behavior: "smooth" });
      return;
    }
    const decrement = readingMode === "double" ? 2 : 1;
    goTo(current - decrement);
  }

  // Guardar progreso en localStorage (por cómic)
  function saveProgress() {
    localStorage.setItem(`progress_${comicId}`, JSON.stringify({ current, readingMode, readingDirection }));
  }

  function loadProgress() {
    const saved = localStorage.getItem(`progress_${comicId}`);
    if (saved) {
      const data = JSON.parse(saved);
      current = data.current || 0;
      readingMode = data.readingMode || "double";
      readingDirection = data.readingDirection || "ltr";
    }
  }

  // Teclado y gestos
  function handleKey(e: KeyboardEvent) {
    if (["INPUT", "TEXTAREA"].includes(document.activeElement?.tagName || "")) return;
    switch (e.key) {
      case "ArrowRight": readingDirection === "ltr" ? next() : prev(); break;
      case "ArrowLeft":  readingDirection === "ltr" ? prev() : next(); break;
      case " ": case "PageDown": e.preventDefault(); next(); break;
      case "PageUp": e.preventDefault(); prev(); break;
      case "Home": goTo(0); break;
      case "End": goTo(pages.length - 1); break;
      case "f": document.documentElement.requestFullscreen?.(); break;
    }
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
    } else {
      document.exitFullscreen();
    }
  }

  onMount(() => {
    loadPages();
    loadProgress();
    window.addEventListener("keydown", handleKey);
    document.addEventListener("fullscreenchange", () => isFullscreen = !!document.fullscreenElement);
  });

  onDestroy(() => {
    window.removeEventListener("keydown", handleKey);
  });
</script>

<svelte:window on:keydown={handleKey} />

<div class="fixed inset-0 bg-black text-white flex flex-col" class:rtl={readingDirection === "rtl"}>
  <!-- Header -->
  <header class="bg-gray-900/95 backdrop-blur p-3 flex justify-between items-center z-50 shrink-0">
    <div class="flex gap-4 items-center">
      <a href="/" class="hover:text-gray-300">Biblioteca</a>
      <button on:click={() => showSidebar = !showSidebar} class="lg:hidden">
        Thumbnails
      </button>
    </div>

    <div class="flex items-center gap-4 text-sm">
      <!-- Modos -->
      <select bind:value={readingMode} on:change={saveProgress} class="bg-gray-800 rounded px-2 py-1">
        <option value="single">Página simple</option>
        <option value="double">Doble página</option>
        <option value="webtoon">Webtoon (scroll)</option>
      </select>

      <select bind:value={readingDirection} on:change={saveProgress} class="bg-gray-800 rounded px-2 py-1">
        <option value="ltr">Occidental (L→R)</option>
        <option value="rtl">Manga (R→L)</option>
      </select>

      <span>{current + 1} / {pages.length}</span>
      <button on:click={toggleFullscreen}>Fullscreen</button>
    </div>
  </header>

  <div class="flex flex-1 overflow-hidden">
    <!-- Sidebar thumbnails -->
    {#if showSidebar}
      <aside class="w-64 bg-gray-900/95 p-4 overflow-y-auto shrink-0 hidden lg:block">
        {#each pages as pageName, i}
          <img
            src={getPageUrl(comicId, i)}
            alt="thumb {i}"
            class="mb-3 cursor-pointer border-4 transition {i === current || (readingMode === 'double' && Math.floor(current/2)*2 === i) ? 'border-blue-500' : 'border-transparent'}"
            on:click={() => goTo(readingMode === 'double' ? Math.floor(i/2)*2 : i)}
          />
        {/each}
      </aside>
    {/if}

    <!-- Visor principal -->
    <main class="flex-1 overflow-auto" class:scroll-smooth={readingMode === "webtoon"}>
      {#if readingMode === "webtoon"}
        <div class="flex flex-col items-center pt-8">
          {#each pages as pageName, i}
            <img src={getPageUrl(comicId, i)} alt="webtoon {i}" class="max-w-full" />
          {/each}
        </div>

      {:else}
        <div class="min-h-screen flex items-center justify-center p-8">
          {#if pages.length > 0}
            {#if readingMode === "double"}
              {@const pair = Math.floor(current / 2) * 2}
              <div class="flex gap-2 max-w-full">
                {#each [pair, pair + 1] as idx}
                  {#if idx < pages.length}
                    <img
                      src={getPageUrl(comicId, readingDirection === "rtl" ? pair + (1 - (idx - pair)) : idx)}
                      alt="page {idx}"
                      class="max-h-screen object-contain cursor-pointer"
                      on:click={next}
                    />
                  {/if}
                {/each}
              </div>
            {:else}
              <img
                src={getPageUrl(comicId, current)}
                alt="page {current}"
                class="max-h-screen max-w-full object-contain cursor-pointer"
                on:click={next}
                on:dblclick={() => document.body.requestFullscreen()}
              />
            {/if}
          {/if}
        </div>
      {/if}
    </main>
  </div>

  <!-- Botones móviles grandes -->
  {#if readingMode !== "webtoon"}
    <button on:click={prev} class="fixed left-4 top-1/2 -translate-y-1/2 text-8xl opacity-30 hover:opacity-70 z-40">Left</button>
    <button on:click={next} class="fixed right-4 top-1/2 -translate-y-1/2 text-8xl opacity-30 hover:opacity-70 z-40">Right</button>
  {/if}
</div>

<style>
  .rtl { direction: rtl; }
  :global(body) { margin: 0; overscroll-behavior: none; }
</style>