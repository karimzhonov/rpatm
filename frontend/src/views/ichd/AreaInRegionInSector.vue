<template>
<div v-if="loading" class="layout-main row justify-content-center">
        <div class="col">
                    <ProgressSpinner style="top:30%; left:47%"/>
                </div>
  </div>
  <div v-if="!loading">
  <BackOrStart :header="area.name" :navigator="[
                {label: `${$t('Сектор')} - ${sector.number}`, to: {name: 'sector_id_region', params: {sector_id: sector_id}, query: $route.query}},
                {label: region.name, to: {name: 'sector_id_region_id_area', params: {sector_id: sector_id, region_id: region_id},  query: $route.query}},
            ]"/>

  <div class="grid row m-1 justify-content-around">
    <div class="card mt-3 rounded-4">
      <div class="col-12">
        <MultiSelect
            :showToggleAll="false"
            v-model="selected"
            :options="options"
            option-label="name"
            placeholder="Select date"
            @change="multiselect_change"
            style="width:100%; color: var(--surface-900)"
            class="mb-3"
        />
        <div class="row">
          <div class="col-12">
            <Bar :series="datasets" :labels="labels" @dataPointSelection="(e, chart, config) => selected_bar(config.dataPointIndex)"/>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
import store from "@/store"
import BackOrStart from "@/components/BackOrStart.vue";
import Bar from "@/components/Bar.vue";
export default {
  name: "AreaInRegionInSector",
  props: ['region_id', 'sector_id', 'area_id'],
  components: {BackOrStart, Bar},
  data() {
    return {
      key: 1,
    }
  },
  methods: {
    async selected_bar(index) {
        const criteria = await store.dispatch('search_criteria', store.state.area_line_chart_labels[index])
        await this.$router.push({
          name: 'sector_id_region_id_area_id_table_id', params: {
            sector_id: this.sector_id, criteria_id: criteria.id,
            region_id: this.region_id, area_id: this.area_id,
          },  query: this.$route.query
        })
    },
    async multiselect_change(e) {
        const files = []
        for (let file of e.value) {
            files.push(file.id)
        }
        if (files.length > 0) {
          await store.dispatch('fetch_area_region_sector', {
              sector: this.sector_id,
              region: this.region_id,
              area: this.area_id,
              chart: true,
              parent_criteria: this.criteria_id,
              file: files.join(','),
            })
          } else {
          store.commit('basic', {key: 'area_line_chart_data', value: []})
          }
    }
  },
  async mounted() {
    await store.dispatch('fetch_sector', this.sector_id)
    await store.dispatch('fetch_region', this.region_id)
    await store.dispatch('fetch_area', this.area_id)
    await store.dispatch('fetch_upload_files')
    await store.dispatch('fetch_area_region_sector', {
      sector: this.sector_id, region: this.region_id, area: this.area_id, chart: true, file: this.$route.query.file
    })
    store.commit('basic', {key: 'loading', value: false})
  },
  computed: {
    sector: () => store.state.sector,
    region: () => store.state.region,
    area: () => store.state.area,
    selected: {
      get: () => store.state.selectedFiles,
      set(value) {
        store.commit('basic', {key: 'selectedFiles', value: value})
      }
    },
    labels: () => store.state.area_line_chart_labels,
    datasets: () =>store.state.area_line_chart_data,
    options: () => store.state.files,
    loading: () => store.state.loading,
  }
}
</script>

<style scoped>

</style>