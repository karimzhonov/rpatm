<template>
    <div v-if="loading" class="layout-main row justify-content-center">
            <div class="col">
                        <ProgressSpinner style="top:30%; left:47%"/>
                    </div>
      </div>
      <div v-if="!loading">
        <BackOrStart :header="$t('По районам')" :navigator="[]"/>
      <div class="card rounded-4">
        <Bar :series="datasets" :labels="labels" @dataPointSelection="async (e, chart, config) => await bar_selected(labels[config.dataPointIndex])"/>
      </div>
    </div>
    </template>
    
<script>
import store from "@/store";
import Bar from "@/components/Bar.vue";
import BackOrStart from "@/components/BackOrStart.vue";

export default {
  name: "RegionView",
  components: {Bar, BackOrStart},
  data() {
    return {
      
    }
  },
  async mounted() {
    await store.dispatch('fetch_region_tables', {file: this.$route.query.file, chart: 'bar'})
    store.commit('basic', {key: 'loading', value: false})
  },
  methods: {
    async bar_selected(region) {
        region = await store.dispatch('search_region', region)
        this.$router.push({name: 'region_id_sector', params: {region_id: region.id}, query: {file: this.$route.query.file, year: this.$route.query.year}})
    },
  },
  computed: {
    datasets: ()=> store.state.region_bar_chart_data,
    labels: () => store.state.region_bar_chart_labels,
    loading: () => store.state.loading,
  }
}
</script>

<style>
.home-main-header {
  margin-bottom: 5rem;
  font-size: 3rem;
  text-transform: uppercase;
  text-align: center;
}
.guide-hover:hover {
  box-shadow: 1px 1px 3px 3px #CCCCCC;
}
</style>
Footer
© 2023 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
