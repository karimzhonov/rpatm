<template>
<div v-if="loading" class="layout-main row justify-content-center">
        <div class="col">
                    <ProgressSpinner style="top:30%; left:47%"/>
                </div>
  </div>
  <div v-if="!loading">
  <BackOrStart :header="`${$t('Сектор')} - ${sector.number}`" :navigator="[
                {label: region.name, to: {name: 'region_id_sector', params: {region_id: region_id}, query: $route.query}},
            ]" :home_to="{name: 'ichd_main', query: this.$route.query}"/>

  <div class="grid row justify-content-around">
    <div class="col-3" v-for="item in areas" :key="item">
      <div class="card p-2">
        <router-link
            :to="{name: 'sector_id_region_id_area_id', params: {sector_id: sector_id, region_id: region_id, area_id: item.area.id}, query: $route.query}"
            class="text-decoration-none speedometer-label">
          <speedometer :value="item.index" :label="item.area.name" :delta_index="item.delta_index"/>
        </router-link>
      </div>
    </div>
  </div>

  <!-- <div class="card rounded-4 mb-3">
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
  </div> -->
  </div>
</template>

<script>
import Speedometer from "@/components/Speedometer.vue";
import BackOrStart from "@/components/BackOrStart.vue";
import store from "@/store"

export default {
  name: "SectorInRegion",
  props: ['region_id', 'sector_id'],
  components: {BackOrStart, Speedometer},
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
      },
    }
  },
  methods: {
    async selected_bar(e) {
      await this.$router.push({name: 'sector_id_region_id_area_id_table_id', params: {id: this.id, table_id: e.element.index}})
    },
    async update_date_range_params() {
    store.commit('basic', {key: 'loading', value: true})
       await store.dispatch('fetch_region_sectors', {region: this.region_id, chart: true, sector: this.sector_id, date_range: `${this.date_range[0].getFullYear()}-${this.date_range[1].getFullYear()}`, chart: 'line'})
    store.commit('basic', {key: 'loading', value: false})
    }
  },
  async mounted() {
    await store.dispatch('fetch_region', this.region_id)
    await store.dispatch('fetch_sector', this.sector_id)
    await store.dispatch('fetch_region_sectors', {region: this.region_id, chart: true, sector: this.sector_id, date_range: `${this.date_range[0].getFullYear()}-${this.date_range[1].getFullYear()}`, chart: 'line'})
    await store.dispatch('fetch_area_region_sector', {region: this.region_id, sector: this.sector_id, chart: false, file: new URL(window.location.href).searchParams.get('file')})
    store.commit('basic', {key: 'loading', value: false})
  },
  computed: {
    region: () => store.state.region,
    sector: () => store.state.sector,
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
    areas: () => store.state.area_region_sector,
    loading: () => store.state.loading,
  },
}
</script>

<style scoped>

</style>