<template>
<div v-if="loading" class="layout-main row justify-content-center">
        <div class="col">
                    <ProgressSpinner style="top:30%; left:47%"/>
                </div>
  </div>
  <div v-if="!loading">
    <BackOrStart :header="$t(criteria.name)" :navigator="[
                {label: `${$t('Сектор')} - ${sector.number}`, to: {name: 'sector_id_region', params: {sector_id: sector_id}, query: $route.query}},
                {label: region.name, to: {name: 'sector_id_region_id_area', params: {sector_id: sector_id, region_id: region_id}, query: $route.query}},
                {label: area.name, to: {name: 'sector_id_region_id_area_id', params: {sector_id: sector_id, region_id: region_id, area_id: area_id}, query: $route.query}},
            ]"/>
  <div class="grid row m-1 justify-content-around">
    <div class="card mt-3 rounded-4">
      <div class="col-12">
        <MultiSelect
            :showToggleAll="false"
            v-model="selected"
            :options="options"
            option-label="name"
            :placeholder="$t('Выберите квартал')"
            @change="multiselect_change"
            style="width:100%; color: var(--surface-900)"
            class="mb-3"
        />
        <div class="row">
          <div class="col">
            <div>
              <DataTable :value="data" showGridlines responsiveLayout="scroll">
                <Column field="file" :header="$t('Квартал')">
                  <template #body="slotProps">
                    <div>{{ slotProps.data[0].file.name }}</div>
                  </template>
                </Column>
                <Column v-for="(col, i) in criteriaes" :key="i" :field="col.name" :header="$t(col.name)">
                  <template #body="slotProps">
                    <div>{{ slotProps.data[i].index }}</div>
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
  name: "CategoryTable",
  props: ['criteria_id', 'region_id', 'sector_id', 'area_id'],
  components: {BackOrStart},
  data() {
    return {
      key: 1,
      basicOptions: {
        plugins: {
          legend: {
            labels: {
              color: '#495057'
            }
          }
        },
        scales: {
          x: {
            ticks: {
              color: '#495057'
            },
            grid: {
              color: '#ebedef'
            }
          },
          y: {
            ticks: {
              color: '#495057'
            },
            grid: {
              color: '#ebedef'
            }
          }
        }
      },
    }
  },
  async mounted() {
    store.commit('basic', {key: 'data', value: []})
    await store.dispatch('fetch_sector', this.sector_id)
    await store.dispatch('fetch_region', this.region_id)
    await store.dispatch('fetch_area', this.area_id)
    await store.dispatch('fetch_criteria', this.criteria_id)
    const files = await store.dispatch('fetch_upload_files')
    await store.dispatch('fetch_criterias', {parent: this.criteria_id})
    await store.dispatch('fetch_main_data', {
      sector: this.sector_id,
      region: this.region_id,
      area: this.area_id,
      chart: true,
      parent_criteria: this.criteria_id,
      file: files[0].id,
    })
    store.commit('basic', {key: 'loading', value: false})
  },
  computed: {
  sector: () => store.state.sector,
    region: () => store.state.region,
    area: () => store.state.area,
    criteria: () => store.state.criteria,
    criteriaes: () => store.state.criteriaChildren,
    selected: {
      get: () => store.state.selectedFiles,
      set(value) {
        store.commit('basic', {key: 'selectedFiles', value: value})
      }
    },
    options: () => store.state.files,
    data: () => store.state.data,
    loading: () => store.state.loading,
  },
  methods: {
    async multiselect_change(e) {
      store.commit('basic', {key: 'data', value: []})
      for (let file of e.value) {
        await store.dispatch('fetch_main_data', {
          sector: this.sector_id,
          region: this.region_id,
          area: this.area_id,
          chart: true,
          parent_criteria: this.criteria_id,
          file: file.id,
        })
      }
    }
  }
}
</script>

<style scoped>

</style>