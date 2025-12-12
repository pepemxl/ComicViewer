<script lang="ts">
  import { browser } from '$app/environment';  // ← ESTO ES LA CLAVE
  import { page } from '$app/stores';
  import { getComicPages, getPageUrl } from "$lib/api";
  import { onMount, onDestroy } from "svelte";

  const comicId = $page.params.id;
  let pages: string[] = [];
  let current = 0;
  let readingDirection = "ltr";
  let readingMode = "double";
  let showSidebar = true;

  // Precarga
  const preloadCache = new Map<number, HTMLImageElement>();

  async function loadPages() {
    const data = await getComicPages(Number(comicId));
    pages = data.pages;
    preloadPagesAround(current);
  }

  function preloadPagesAround(center: number) {
    const range = 4;
    for (let i = Math.max(0, center - range); i < Math.min(pages.length, center + range + 4); i++) {
      if (!preloadCache.has(i)) {
        const img = new Image();
        img.src = getPageUrl(Number(comicId), i);
        preloadCache.set(i, img);
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
      if (browser) window.scrollBy({ top: window.innerHeight * 0.9, behavior: "smooth" });
      return;
    }
    const inc = readingMode === "double" ? 2 : 1;
    goTo(current + inc);
  }

  function prev() {
    if (readingMode === "webtoon") {
      if (browser) window.scrollBy({ top: -window.innerHeight * 0.9, behavior: "smooth" });
      return;
    }
    const dec = readingMode === "double" ? 2 : 1;
    goTo(current - dec);
  }

  function saveProgress() {
    if (!browser) return;
    localStorage.setItem(`progress_${comicId}`, JSON.stringify({ current, readingMode, readingDirection }));
  }

  function loadProgress() {
    if (!browser) return;
    const saved = localStorage.getItem(`progress_${comicId}`);
    if (saved) {
      const data = JSON.parse(saved);
      current = data.current || 0;
      readingMode = data.readingMode || "double";
      readingDirection = data.readingDirection || "ltr";
    }
  }

  function handleKey(e: KeyboardEvent) {
    if (!browser) return;
    switch (e.key) {
      case "ArrowRight": readingDirection === "ltr" ? next() : prev(); break;
      case "ArrowLeft":  readingDirection === "ltr" ? prev() : next(); break;
      case " ": case "PageDown": e.preventDefault(); next(); break;
      case "PageUp": e.preventDefault(); prev(); break;
    }
  }

  onMount(() => {
    loadPages();
    loadProgress();
    if (browser) window.addEventListener("keydown", handleKey);
  });

  onDestroy(() => {
    if (browser) window.removeEventListener("keydown", handleKey);
  });
</script>

<svelte:window on:keydown={handleKey} />

<!-- El resto del HTML queda IGUAL, solo arreglamos 3 líneas con role + tabindex -->
<div class="fixed inset-0 bg-black text-white flex flex-col" class:rtl={readingDirection === "rtl"}>
  <header class="bg-gray-900/95 backdrop-blur p-3 flex justify-between items-center z-50 shrink-0">
    <!-- ... mismo header ... -->
  </header>

  <div class="flex flex-1 overflow-hidden">
    {#if showSidebar}
      <aside class="w-64 bg-gray-900/95 p-4 overflow-y-auto shrink-0 hidden lg:block">
        {#each pages as pageName, i}
          <!-- Arreglado A11Y: div → button + role + tabindex -->
          <button
            class="block mb-3 border-4 transition {i === current ? 'border-blue-500' : 'border-transparent'}"
            on:click={() => goTo(readingMode === 'double' ? Math.floor(i/2)*2 : i)}
          >
            <img src={getPageUrl(Number(comicId), i)} alt="Miniatura página {i + 1}" class="w-full" />
          </button>
        {/each}
      </aside>
    {/if}

    <main class="flex-1 overflow-auto" class:scroll-smooth={readingMode === "webtoon"}>
      {#if readingMode === "webtoon"}
        <div class="flex flex-col items-center pt-8">
          {#each pages as pageName, i}
            <img src={getPageUrl(Number(comicId), i)} alt="Página {i + 1}" class="max-w-full" />
          {/each}
        </div>
      {:else if readingMode === "double"}
        {@const pair = Math.floor(current / 2) * 2}
        <div class="min-h-screen flex items-center justify-center p-8 gap-2">
          {#each [pair, pair + 1] as idx}
            {#if idx < pages.length}
              <img
                src={getPageUrl(Number(comicId), readingDirection === "rtl" ? pair + (1 - (idx - pair)) : idx)}
                alt="Página {idx + 1}"
                class="max-h-screen object-contain cursor-pointer"
                on:click={next}
                role="button"
                tabindex="0"
                on:keydown={(e) => e.key === "Enter" && next()}
              />
            {/if}
          {/each}
        </div>
      {:else}
        <div class="min-h-screen flex items-center justify-center p-8">
          <img
            src={getPageUrl(Number(comicId), current)}
            alt="Página {current + 1}"
            class="max-h-screen max-w-full object-contain cursor-pointer"
            on:click={next}
            role="button"
            tabindex="0"
            on:keydown={(e) => e.key === "Enter" && next()}
          />
        </div>
      {/if}
    </main>
  </div>
</div>