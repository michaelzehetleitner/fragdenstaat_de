<template>
  <SearchBar @search="handleSearch" class="mb-4" />
  <div v-if="searchParams">
    <template v-if="searchResults === null">
       <div class="spinner-border" role="status"></div>
    </template>
    <template v-else-if="searchResults.length > 0">
      <SearchResult v-for="result in searchResults" :key="result.id" v-bind="result" />
    </template>
    <div v-else>No results</div>
    <div>
      <button :disabled="searchParams.currentPage === 0" @click="searchParams.currentPage--">&lt;</button>
      {{ searchParams?.currentPage + 1 }}
      <button :disabled="searchParams.currentPage >= searchParams.maxPage"
        @click="searchParams.currentPage++">&gt;</button>
    </div>
  </div>
  <div v-else>Enter search term and click search</div>
</template>

<script lang="ts" setup>
import SearchBar from './search-bar.vue'
import SearchResult from './search-result.vue'
import DOMPurify from 'dompurify';
import { defineProps, ref, watch, onWatcherCleanup, Ref } from 'vue'

const ITEMS_PER_PAGE = 10;

export type Result = { title: string, url: string, id: string, text: string, site: string };
type SearchParams = { query: string, currentPage: number, maxPage: number }

const props = defineProps<{ endpoint: string }>()

const searchParams: Ref<SearchParams | null> = ref(null);
const searchResults: Ref<Result[] | null> = ref(null);

function handleSearch(search: string) {
  searchParams.value = { query: search, currentPage: 0, maxPage: 0 }
}

watch((): [string | undefined, number | undefined] => [searchParams.value?.query, searchParams.value?.currentPage], ([query, page] : [string | undefined, number | undefined]) => {
  if (query !== undefined) {
    searchResults.value = null;

    const controller = new AbortController()

    const searchUrl = new URL(props.endpoint);
    if (page) {
      searchUrl.searchParams.set('p', (page * ITEMS_PER_PAGE).toString())
    }
    searchUrl.searchParams.set('q', query)
    searchUrl.searchParams.set('n', ITEMS_PER_PAGE.toString())
    

    fetch(searchUrl, { signal: controller.signal }).then((response) => response.text())
      .then((text) => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, "text/xml");
        searchResults.value = Array.from(doc.getElementsByTagName("item")).map(item => {
          const result = {
            title: item.getElementsByTagName('title')[0].textContent!,
            url: item.getElementsByTagName('link')[0].textContent!,
            id: item.getElementsByTagName('docId')[0].textContent!,
            text: DOMPurify.sanitize(item.getElementsByTagName('description')[0].textContent!),
            site: item.getElementsByTagName('site')[0].textContent!
          };
          return result
        });
        searchParams.value!.maxPage = parseInt(doc.getElementsByTagName('totalResults')[0].textContent!)/parseInt(doc.getElementsByTagName('itemsPerPage')[0].textContent!)
      });

    onWatcherCleanup(() => {
      controller.abort()
    })
  }
})

</script>
