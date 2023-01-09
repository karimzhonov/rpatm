<template>
  <BackOrStart :header="`${$t('Сектор')} - ${sector.number}`" :navigator="[
                {label: `${$t('Сектор')} - ${sector.number}`, to: {name: 'sector_id_region', params: {sector_id: sector_id}}},
            ]"/>

  <div class="grid">
    <div class="col-9">
      <div class="card rounded-4">
        <Chart type="line" :data="basicData" :options="basicOptions"/>
      </div>
    </div>
    <div class="col-3">
      <div class="card rounded-4">
        <h5 class="text-center mb-3">{{ $t("Филтеры") }}</h5>
        <p>{{ $t("Период") }}</p>
        <Calendar v-model="date_range" dateFormat="dd.mm.yy" selectionMode="range" view="year"
                  @date-select="update_date_range_params"/>
        <p>{{ $t("Критерия") }}</p>
        <Listbox v-model="selectedCriteria" :options="criteria" optionLabel="label" :multiple="true"/>
      </div>
    </div>
  </div>
  <div class="card rounded-4 mb-3">
    <h2 class="text-center m-0">{{ $t("Регионы") }}</h2>
  </div>
  <div class="grid justify-content-around">
    <div class="col-3" v-for="item in region_sectors" :key="item.id">
      <div class="card p-2">
        <router-link :to="{name: 'sector_id_region_id_area', params: {sector_id: sector_id, region_id: item.region.id}}"
                     class="text-decoration-none speedometer-label">
          <speedometer :value="item.index" :label="item.region.name" :delta_index="item.delta_index"/>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import Speedometer from "@/components/Speedometer.vue";
import BackOrStart from "@/components/BackOrStart.vue";
import store from "@/store";

export default {
  name: "Category",
  props: ['sector_id'],
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
  async mounted() {
    await store.dispatch('fetch_sector', this.sector_id)
    await store.dispatch('fetch_sector_tables', {sector: this.sector_id})
    await store.dispatch('fetch_region_sectors', {sector: this.sector_id, file: 0, chart: false})
  },
  methods: {
    update_date_range_params() {
      console.log(this.date_range)
    }
  },
  computed: {
    sector: () => store.state.sector,
    basicData() {
      return {
        labels: store.state.sector_line_chart_labels,
        datasets: store.state.selectedSectorCriteria
      }
    },
    criteria: () => store.state.sector_line_chart_data,
    selectedCriteria: {
      get: () => store.state.selectedSectorCriteria,
      set(value) {
        store.commit('basic', {key: 'selectedSectorCriteria', value: value})
      }
    },
    region_sectors: () => store.state.region_sectors
  }
}
</script>

<style scoped>

</style>