<template>
    <div v-if="loading" class="layout-main row justify-content-center">
        <div class="col">
            <ProgressSpinner style="top:30%; left:47%"/>
        </div>
    </div>
    <div v-if="!loading">
        <div class="row">
            <div class="col-3" v-for="region in regions" :key="region.id">
                <RouterLink :to="{name: 'passport_region_data', query: $route.query, params: {region_id: region.id}}">
                    <div class="card rounded-4">
                        <img :src="region.image" :alt="region.name"/>
                        <h4 class="text-center">{{ region.name }}</h4>
                    </div>
                </RouterLink>
            </div>
        </div>
    </div>
</template>
<script>
import store from '@/store';
    export default {
        name: 'Layout',
        async mounted() {
            await store.dispatch('fetch_regions_passport')
            store.commit('basic', {key: 'loading', value: false})
        },
        computed: {
            loading: () => store.state.loading,
            regions: () => store.state.regions,
        }
    }
</script>