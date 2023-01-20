<template>
    <div v-if="loading" class="layout-main row justify-content-center">
            <div class="col">
                        <ProgressSpinner style="top:30%; left:47%"/>
                    </div>
      </div>
      <div v-if="!loading">
        <BackOrStart :header="`${region.name} (${criteria.name})`" :navigator="[
          {label: $t('Районы'), to: {name: 'ichd_region-data-table', query: {file: $route.query.file, year: $route.query.year, criteria: $route.query.criteria}}},
        ]" :home_to="{name: 'ichd_main', query: this.$route.query}"/>
        <div class="card mt-3 rounded-4">
          <div class="col-12">
            <div class="row">
              <div class="col">
                <div>
                    <DataTable :value="data" showGridlines responsiveLayout="scroll">
                        <Column field="area">
                          <template #header>
                            <p style="font-size: 1.5rem;" class="text-center m-auto">{{ $t('Махалла') }}</p>
                          </template>
                          <template #body="slotProps">
                            <p class="text-center" style="font-size: 1.5rem">{{ slotProps.data.name }}</p>
                        </template>
                        </Column>
                        <Column v-for="(col, i) in criteriaes" :key="i" :field="col.name">
                          <template #header>
                            <p class="text-center m-auto" style="font-size: 1.3rem">{{ $t(col.name) }}</p>
                          </template>
                        <template #body="slotProps">
                            <p class="text-center" style="font-size: 1.5rem">
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
        name: 'AreaDataTableView',
        components: {BackOrStart},
        async mounted() {
            await store.dispatch('fetch_criteria', this.$route.query.criteria)
            await store.dispatch('fetch_region', this.$route.query.region)
            await store.dispatch('fetch_criterias', {parent: this.$route.query.criteria})
            await store.dispatch('fetch_area_table_data', {file: this.$route.query.file, parent_criteria: this.$route.query.criteria, main_criteria: true, region: this.$route.query.region})
            store.commit('basic', {key: 'loading', value: false})
        },
        computed: {
          criteria: () => store.state.criteria,
            region: () => store.state.region,
            criteriaes: () => store.state.criteriaChildren,
            data: () => store.state.area_table_data,
            loading: () => store.state.loading
        }
    }
    </script>