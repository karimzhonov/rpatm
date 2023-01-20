<template>
<div v-if="loading" class="layout-main row justify-content-center">
    <div class="col">
        <ProgressSpinner style="top:30%; left:47%"/>
    </div>
</div>
<div v-if="!loading">
    <BackOrStart :header="region.name" :navigator="[]" :home_to="{name: 'passport_main', query: this.$route.query}"/>
    <div class="card rounded-4">
        <h2 class="text-center font-weight-bold text-decoration-underline">I. {{ $t('Ключевые показатели') }}</h2>
        <div class="row">
            <div class="col-6">
                <img style="width: 100%" :src="region.image" :alt="region.name">
            </div>
            <div class="col-6"></div>
        </div>
    </div>
    <div class="card rounded-4">
        <h2 class="text-center font-weight-bold text-decoration-underline">II. {{ $t('Макроэкономические показатели') }}</h2>
        <div class="row">
            <div class="col-6">
                
            </div>
            <div class="col-6">

            </div>
        </div>
    </div>
</div>
</template>
<script>
import BackOrStart from '@/components/BackOrStart.vue';
import store from '@/store';

export default {
    name: 'RegionDataView',
    props: ['region_id'],
    components: {BackOrStart},
    async mounted() {
        await store.dispatch('fetch_region_passport', this.region_id)
        await store.dispatch('fetch_data_table_passport', {file: this.$route.query.file, region: this.$route.region_id})
        store.commit('basic', {key: 'loading', value: false})
    },
    computed: {
        region: () => store.state.region,
        loading: () => store.state.loading,
        data: () => store.state.data,
    },
    // methods: {
    //     _(text) {
    //         for (let row of this.data) {
    //             if (text == row.)
    //         }
    //     }
    // }
}
</script>