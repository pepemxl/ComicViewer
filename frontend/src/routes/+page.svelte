<script lang="ts">
  import { onMount } from "svelte";
  import { getComics, uploadComic } from "$lib/api";

  let comics: any[] = [];
  let fileInput: HTMLInputElement;

  async function loadComics() {
    comics = await getComics();
  }

  async function handleUpload() {
    if (!fileInput.files?.length) return;
    await uploadComic(fileInput.files[0]);
    fileInput.value = "";
    loadComics();
  }

  onMount(loadComics);
</script>

<main class="p-6 max-w-7xl mx-auto">
  <h1 class="text-4xl font-bold mb-8 text-center">Cómics/Mangas/Manhwas</h1>

  <!-- Upload -->
  <div class="mb-8 text-center">
    <input type="file" accept=".cbz" bind:this={fileInput} class="hidden" on:change={handleUpload} />
    <button 
      on:click={() => fileInput.click()}
      class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg text-lg">
      Subir nuevo .cbz
    </button>
  </div>

  <!-- Grid -->
  <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-6">
    {#each comics as comic}
        <span>comic {comic.title} {comic.filename}</span>
      <a href="/comic/{comic.id}" class="group block">
        <div class="bg-gray-800 rounded-lg overflow-hidden shadow-lg hover:shadow-2xl transition">
          {#if comic.pages > 0}
            <img 
              src="{`http://localhost:8000/comics/${comic.id}/page/0`}" 
              alt="{comic.title}"
              class="w-full h-64 object-cover group-hover:scale-105 transition"
            />
          {:else}
            <div class="w-full h-64 bg-gray-700 flex items-center justify-center">
              <span class="text-gray-500">Sin portada</span>
            </div>
          {/if}
          <div class="p-3">
            <p class="text-sm font-medium truncate">{comic.title}</p>
            <p class="text-xs text-gray-400">{comic.pages} páginas</p>
          </div>
        </div>
      </a>
    {/each}
  </div>
</main>