<template>
<div v-if="loading" class="layout-main row justify-content-center">
        <div class="col">
                    <ProgressSpinner style="top:30%; left:47%"/>
                </div>
  </div>
  <div v-if="!loading">
    <BackOrStart :header="$t('Махаллы')" :navigator="[]"/>
    <div class="card mt-3 rounded-4">
      <div class="col-12">
        <div class="row">
          <div class="col">
            <div>
                <data-table :value="data" showGridlines responsiveLayout="scroll">
                <column field="number" :header="$t('Место')">
                  <template #body="slotProps">
                    <div>{{ data.indexOf(slotProps.data) + 1}}</div>
                  </template>
                </column>
                <column field="sector" :header="$t('Сектор')">
                  <template #body="slotProps">
                    <div>{{ slotProps.data.sector.number}}</div>
                  </template>
                </column>
                <column field="region" :header="$t('Район')">
                  <template #body="slotProps">
                    <div>{{ slotProps.data.region.name}}</div>
                  </template>
                </column>
                <column field="area" :header="$t('Махалла')">
                  <template #body="slotProps">
                    <div>{{ slotProps.data.area.name}}</div>
                  </template>
                </column>
                <column field="index" :header="$t('ИЧД')">
                  <template #body="slotProps">
                    <div>{{ slotProps.data.index}}</div>
                  </template>
                </column>
              </data-table>
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
    name: 'DataTableView',
    components: {BackOrStart},
    async mounted() {
        await store.dispatch('fetch_data_table', {...this.$route.query, main_criteria: true})
        store.commit('basic', {key: 'loading', value: false})
    },
    computed: {
        data: () => store.state.data_table,
        loading: () => store.state.loading
    }
}
</script>