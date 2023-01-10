<template>
<div v-if="loading" class="layout-main row justify-content-center">
        <div class="col">
                    <ProgressSpinner style="top:30%; left:47%"/>
                </div>
  </div>
  <div v-if="!loading">
    <BackOrStart :header="region.name" :navigator="[
                {label: region.name, to: {name: 'region_id_sector', params: {region_id: region_id}}},
            ]"/>

  <div class="grid row justify-content-around">
    <div class="col-3" v-for="item in region_sectors" :key="item">
      <div class="card p-2">
        <router-link :to="{name: 'region_id_sector_id', params: {sector_id: item.sector.id, region_id: region_id}}"
                     class="text-decoration-none speedometer-label">
          <speedometer :value="item.index" :label="`${$t('Сектор')} - ${item.sector.number}`" :delta_index="item.delta_index"/>
        </router-link>
      </div>
    </div>
  </div>

  <div class="card rounded-4 mb-3">
    <h2 class="text-center m-0">{{ $t("Изменения индекса") }}</h2>
  </div>

  <div class="grid">
    <div class="col-9">
      <div class="card mt-3 rounded-4">
        <Chart type="line" :data="basicData" :options="basicOptions"/>
      </div>
    </div>
    <div class="col-3">
      <div class="card mt-3 rounded-4">
        <Calendar v-model="date_range" dateFormat="yy" selectionMode="range"
                  @date-select="update_date_range_params" view='year'/>
        <p>{{ $t("Критерия") }}</p>
        <Listbox v-model="selectedCriteria" :options="criteria" optionLabel="label" :multiple="true"/>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
import Speedometer from "@/components/Speedometer.vue";
import BackOrStart from "@/components/BackOrStart.vue";
import store from "@/store"

export default {
  name: "Region",
  props: ['region_id'],
  components: {Speedometer, BackOrStart},
  data() {
    return {
      params: {},
      date_range: [new Date(new Date().setFullYear(new Date().getFullYear() - 1)), new Date()],
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
      }
    }
  },
 async mounted() {
    await store.dispatch('fetch_region', this.region_id)
    await store.dispatch('fetch_region_tables', {region: this.region_id, date_range: `${this.date_range[0].getFullYear()}-${this.date_range[1].getFullYear()}`, chart: 'line'})
    await store.dispatch('fetch_region_sectors', {region: this.region_id, chart: false, file: 0})
    store.commit('basic', {key: 'loading', value: false})
 },
  computed: {
    region: () => store.state.region,
    basicData() {
      return {
        labels: store.state.region_line_chart_labels,
        datasets: store.state.selectedRegionCriteria
      }
    },
    criteria: () => store.state.region_line_chart_data,
    selectedCriteria: {
      get: () => store.state.selectedRegionCriteria,
      set(value) {
        store.commit('basic', {key: 'selectedRegionCriteria', value: value})
      }
    },
    region_sectors: () => store.state.region_sectors,
    loading: () => store.state.loading,
  },
  methods: {
    async update_date_range_params() {
      store.commit('basic', {key: 'loading', value: true})
      await store.dispatch('fetch_region_tables', {region: this.region_id, date_range: `${this.date_range[0].getFullYear()}-${this.date_range[1].getFullYear()}`, chart: 'line'})
      store.commit('basic', {key: 'loading', value: false})
    }
  },
}
</script>

<style scoped>

</style>