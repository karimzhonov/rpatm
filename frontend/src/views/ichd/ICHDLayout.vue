<template>
<div class="row mr-3 ml-3 justify-content-end align-items-center">
    <div class="col-9">
        <div>
            <div class="home-main-header mb-1">
                <img style="color: var(--surface-900)" class="mr-2" :src="logo" width="150"/>
                {{ $t("Индекс человеческого достоинства") }}
            </div>
        </div>
    </div>
    <div class="col-2">
        <Dropdown class="ml-3" :options="selected_year.files" optionLabel="name"
                :model-value="selected_file"
                @change="file_change" inputStyle="padding: 1rem"
      />
    </div>
    <div class="col-1">
        <Dropdown class="ml-3" :options="top_bar_years" optionLabel="year"
                :model-value="selected_year"
                @change="year_change" inputStyle="padding: 1rem"
      />
    </div>
</div>
<RouterView></RouterView>
</template>
<script>
import store from '@/store';
import logo_light from "@/assets/images/logo minimalis.svg"
import logo_dark from "@/assets/images/logo minimalist light (1).svg"
export default {
    name: 'ICHDLoyaut',
    data() {
        return {
            logo_dark, logo_light,
        }
    },
    async mounted() {
        await store.dispatch('fetch_top_bar_files')
    },
    computed: {
        top_bar_years: () => store.state.top_bar_years,
        selected_file: () => store.state.selected_file,
        selected_year: () => store.state.selected_year,
        logo() {
            return !store.state.darkMode ? this.logo_light : this.logo_dark
        }
    },
    methods: {
        year_change(e) {
            store.commit('basic', {key: 'selected_year', value: e.value})
        },
        file_change(e) {
            const url = new URL(window.location)
            url.searchParams.set('file', e.value.id)
            window.location = url
            store.commit('basic', {key: 'selected_file', value: e.value})
        },
    }
}
</script>

<style>

.home-main-header {
  margin-bottom: 5rem;
  font-size: 2.5rem;
  text-transform: uppercase;
  text-align: center;
  line-height: 70px;
  color: var(--surface-900);
}
</style>