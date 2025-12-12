<script lang="ts">
  import { onMount } from "svelte";
  import { getComics } from "$lib/api";

  let allComics = [];
  let seriesList = [];
  let selectedSeries = null;
  let search = "";

  async function load() {
    allComics = await getComics();
    const groups = {};
    allComics.forEach(c => {
      const s = c.series || "Sin serie";
      if (!groups[s]) groups[s] = [];
      groups[s].push(c);
    });
    
    seriesList = Object.entries(groups).map(([name, comics]) => {
      comics.sort((a,b) => a.volume - b.volume);
      return {
        name,
        comics,
        cover: comics[0],
        count: comics.length
      };
    }).sort((a,b) => a.name.localeCompare(b.name));
  }

  $: filteredSeries = seriesList.filter(s => 
    s.name.toLowerCase().includes(search.toLowerCase())
  );

  onMount(load);
</script>

<main class="min-h-screen bg-gray-950 text-white p-6">
  <div class="max-w-7xl mx-auto">
    <h1 class="text-5xl font-bold mb-8 text-center">Mi Biblioteca</h1>

    <!-- Buscador + botón escanear -->
    <div class="flex gap-4 mb-8 justify-center flex-wrap">
      <input 
        type="text" 
        bind:value={search}
        placeholder="Buscar serie..."
        class="px-6 py-3 rounded-lg bg-gray-800 text-lg w-96"
      />
      <button 
        on:click={() => fetch("http://localhost:8000/scan", {method: "POST"}).then(load)}
        class="bg-green-600 hover:bg-green-700 px-6 py-3 rounded-lg">
        Escanear carpeta
      </button>
    </div>

    <!-- Grid de series -->
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-6">
      {#each filteredSeries as serie}
        <div class="group cursor-pointer" on:click={() => selectedSeries = serie}>
          <div class="bg-gray-900 rounded-xl overflow-hidden shadow-2xl hover:shadow-blue-500/50 transition">
            {#if serie.cover}
              <img 
                src={`http://localhost:8000/comics/${serie.cover.id}/page/0`}
                alt={serie.name}
                class="w-full aspect-[2/3] object-cover group-hover:scale-105 transition"
              />
            {/if}
            <div class="p-4">
              <h3 class="font-bold text-sm truncate">{serie.name}</h3>
              <p class="text-xs text-gray-400">{serie.count} volúmenes</p>
            </div>
          </div>
        </div>
      {/each}
    </div>

    <!-- Modal de serie -->
    {#if selectedSeries}
      <div class="fixed inset-0 bg-black/90 z-50 flex items-center justify-center p-8" on:click={() => selectedSeries = null}>
        <div class="max-w-6xl max-h-full overflow-y-auto bg-gray-900 rounded-2xl p-8" on:click|stopPropagation>
          <h2 class="text-4xl font-bold mb-8">{selectedSeries.name}</h2>
          <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-6">
            {#each selectedSeries.comics as comic}
              <a href="/comic/{comic.id}" class="block group">
                <img 
                  src={`http://localhost:8000/comics/${comic.id}/page/0`}
                  class="w-full aspect-[2/3] object-cover rounded-lg shadow-lg group-hover:shadow-blue-500 transition"
                />
                <p class="text-center mt-2 text-sm">{comic.title.replace(/^.* - /, "")}</p>
              </a>
            {/each}
          </div>
          <button 
            class="mt-8 bg-red-600 hover:bg-red-700 px-6 py-3 rounded-lg"
            on:click={() => selectedSeries = null}>
            Cerrar
          </button>
        </div>
      </div>
    {/if}
  </div>
</main>