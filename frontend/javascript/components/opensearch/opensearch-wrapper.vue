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

const props = defineProps<{ endpoint: string, urltemplate: string }>()

const searchParams: Ref<SearchParams | null> = ref(null);
const searchResults: Ref<Result[] | null> = ref(null);

function handleSearch(search: string) {
  searchParams.value = { query: search, currentPage: 0, maxPage: 0 }
}

function getElementContent(item: Element | Document, tagName: string): string {
  return item.getElementsByTagName(tagName)[0].textContent!
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
          const date = getElementContent(item, 'date')
          const link = getElementContent(item, 'link')
          const collection = getElementContent(item, 'collection')
          const result = {
            title: getElementContent(item, 'title'),
            url: props.urltemplate.replace('$collection', collection).replace('$link', link).replace('$date', date),
            id: getElementContent(item, 'docId'),
            text: DOMPurify.sanitize(getElementContent(item, 'description')),
            site: getElementContent(item, 'site')
          };
          return result
        });
        searchParams.value!.maxPage = parseInt(getElementContent(doc, 'totalResults'))/parseInt(getElementContent(doc, 'itemsPerPage'))
      });

    onWatcherCleanup(() => {
      controller.abort()
    })
  }
})

</script>
