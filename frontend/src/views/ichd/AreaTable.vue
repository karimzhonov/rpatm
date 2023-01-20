<template>
<div v-if="loading" class="layout-main row justify-content-center">
        <div class="col">
                    <ProgressSpinner style="top:30%; left:47%"/>
                </div>
  </div>
  <div v-if="!loading">
    <BackOrStart :header="$t(criteria.name)" :navigator="[
                {label: `${$t('Сектор')} - ${sector.number}`, to: {name: 'ichd_sector_id_region_id', params: {sector_id: sector_id}, query: $route.query}},
                {label: region.name, to: {name: 'sector_id_region_id_area', params: {sector_id: sector_id, region_id: region_id}, query: $route.query}},
            ]" :home_to="{name: 'ichd_main', query: this.$route.query}"/>
  <div class="grid row m-1 justify-content-around">
    <div class="card mt-3 rounded-4">
      <div class="col-12">
        <div class="row">
          <div class="col">
            <div>
              <DataTable :value="data" showGridlines responsiveLayout="scroll">
                <Column field="area" :header="$t('Махалла')">
                    <template #body="slotProps">
                    <div>{{ slotProps.data.name }}</div>
                  </template>
                </Column>
                <Column v-for="(col, i) in criteriaes" :key="i" :field="col.name" :header="$t(col.name)">
                  <template #body="slotProps">
                    <div>
                        {{ slotProps.data.data[i].index }}
                    </div>
                  </template>
                </Column>
              </DataTable>
            </div>
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

export default {
  name: "AreaTableView",
  props: ['region_id', 'sector_id', 'criteria_id'],
  components: {BackOrStart},
  data() {
    return {
    }
  },
  async mounted() {
    store.commit('basic', {key: 'data', value: []})
    await store.dispatch('fetch_sector', this.sector_id)
    await store.dispatch('fetch_region', this.region_id)
    await store.dispatch('fetch_criteria', this.criteria_id)
    await store.dispatch('fetch_criterias', {parent: this.criteria_id})
    await store.dispatch('fetch_area_table_data', {
      sector: this.sector_id,
      region: this.region_id,
      parent_criteria: this.criteria_id,
      file: this.$route.query.file,
    })
    store.commit('basic', {key: 'loading', value: false})
  },
  computed: {
  sector: () => store.state.sector,
    region: () => store.state.region,
    area: () => store.state.area,
    criteria: () => store.state.criteria,
    criteriaes: () => store.state.criteriaChildren,
    data: () => store.state.area_table_data,
    loading: () => store.state.loading,
  },
  methods: {
  }
}
</script>