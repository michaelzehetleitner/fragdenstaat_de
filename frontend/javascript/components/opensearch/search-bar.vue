<template>
    <form class="row" role="search" @submit.prevent="(event) => $emit('search', event.target.search.value)">
        <div class="col">
            <div class="input-group">
                <input class="form-control" type="text" name="search" placeholder="{% translate 'Search' %}"
                    aria-label="{% translate 'Search' %}">
                <button class="btn btn-outline-primary" type="submit">
                    <i class="fa fa-search" aria-hidden="true"></i>
                    {% translate 'Search' %} <!-- TODO: i18n -->
                </button>
            </div>
        </div>
    </form>
</template>
