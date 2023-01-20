<template>
    <div v-if="loading" class="layout-main row justify-content-center">
            <div class="col">
                        <ProgressSpinner style="top:30%; left:47%"/>
                    </div>
      </div>
      <div v-if="!loading">
        <BackOrStart :header="`${$t('Районы')} (${$t(criteria.name)})`" :navigator="[]" :home_to="{name: 'ichd_main', query: this.$route.query}"/>
        <div class="card mt-3 rounded-4">
          <div class="col-12">
            <div class="row">
              <div class="col">
                <div>
                    <DataTable :value="data" showGridlines responsiveLayout="scroll">
                        <Column field="area">
                          <template #header>
                            <p style="font-size: 1.5rem;" class="text-center m-auto">{{ $t('Район') }}</p>
                          </template>
                          <template #body="slotProps">
                            <p class="text-center cursor-pointer" style="font-size: 1.5rem" @click="async () => await row_click(slotProps.data.id)">{{ slotProps.data.name }}</p>
                        </template>
                        </Column>
                        <Column v-for="(col, i) in criteriaes" :key="i" :field="col.name">
                          <template #header>
                            <p class="text-center m-auto" style="font-size: 1.3rem">{{ $t(col.name) }}</p>
                          </template>
                        <template #body="slotProps">
                          <p class="text-center cursor-pointer" style="font-size: 1.5rem" @click="async () => await row_click(slotProps.data.id)">
                                {{ slotProps.data.data[i].index }}
                          </p>
                        </template>
                        </Column>
                    </DataTable>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <script>
import store from '@/store';
import BackOrStart from '@/components/BackOrStart.vue';
export default {
    name: 'RegionDataTableView',
    components: {BackOrStart},
    async mounted() {
        await store.dispatch('fetch_criteria', this.$route.query.criteria)
        await store.dispatch('fetch_criterias', {parent: this.$route.query.criteria})
        await store.dispatch('fetch_region_data_table', {file: this.$route.query.file, parent_criteria: this.$route.query.criteria, main_criteria: true})
        store.commit('basic', {key: 'loading', value: false})
    },
    methods: {
      async row_click(region_id) {
        await this.$router.push({'name': 'ichd_area-data-table', query: {...this.$route.query, region: region_id}})
        console.log(region_id)
      }
    },
    computed: {
        criteria: () => store.state.criteria,
        criteriaes: () => store.state.criteriaChildren,
        data: () => store.state.region_data_table,
        loading: () => store.state.loading
    }
}
</script>