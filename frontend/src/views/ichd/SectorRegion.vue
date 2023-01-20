<template>
<div v-if="loading" class="layout-main row justify-content-center">
    <div class="col">
        <ProgressSpinner style="top:30%; left:47%"/>
    </div>
</div>
<div v-if="!loading">
    <BackOrStart :header="region.name" :navigator="[
                {label: `${$t('Сектор')} - ${sector.number}`, to: {name: 'sector_id_region', params: {sector_id: sector_id}, query: $route.query}},
            ]" :home_to="{name: 'ichd_main', query: this.$route.query}"/>
    <div class="card rounded-4" v-for="bar in sector_region_bar_chart_data" :key="bar">
        <Bar :series="bar.datasets" :labels="bar.labels" @dataPointSelection="(e, chart, config) => bar_selected(bar.labels[config.dataPointIndex])"/>
    </div>
</div>
</template>
<script>
import store from '@/store';
import BackOrStart from '@/components/BackOrStart.vue';
import Bar from '@/components/Bar.vue';

export default {
    name: 'Region',
    props: ['region_id', 'sector_id'],
    components: {BackOrStart, Bar},
    async mounted() {
        await store.dispatch('fetch_region', this.region_id)
        await store.dispatch('fetch_sector', this.sector_id)
        await store.dispatch('fetch_sector_region_bar_chart_data', {sector: this.sector_id, region: this.region_id, file: this.$route.query.file})
        store.commit('basic', {key: 'loading', value: false})
    },
    methods: {
        async bar_selected(criteria) {
            criteria = await store.dispatch('search_criteria', criteria)
            this.$router.push({name: 'ichd_sector_id_region_id_criteria_id', params: {sector_id: this.sector_id, region_id: this.region_id, criteria_id: criteria.id}, query: {file: this.$route.query.file, year: this.$route.query.year}})
        }
    },
    computed: {
        loading: () => store.state.loading,
        region: () => store.state.region,
        sector: () => store.state.sector,
        sector_region_bar_chart_data: () => store.state.sector_region_bar_chart_data
    }
}
</script>