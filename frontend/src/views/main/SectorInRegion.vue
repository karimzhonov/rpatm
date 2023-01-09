<template>
  <BackOrStart/>
  <h2 class="text-center">Сектор - {{sector_id}}</h2>
  <div class="grid">
    <div class="col-9">
      <div class="card mt-3 rounded-4">
        <Chart type="line" :data="basicData" :options="basicOptions"/>
      </div>
    </div>
    <div class="col-3">
      <div class="card mt-3 rounded-4">
        <Calendar v-model="date_range" dateFormat="dd.mm.yy" selectionMode="range"
                  @date-select="update_date_range_params"/>
      </div>
    </div>
  </div>
  <h2 class="text-center">Махалла</h2>
  <div class="grid row m-3 justify-content-around">
    <div class="col-3" v-for="item in [1, 2, 3, 4]" :key="item">
      <div class="card p-2">
        <router-link
            :to="{name: 'sector_id_region_id_area_id', params: {sector_id: 1, region_id: region_id, area_id: item}}"
            class="text-decoration-none speedometer-label">
          <speedometer :value="0.6" :label="`Махалла ${item}`"/>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import Speedometer from "@/components/Speedometer.vue";
import BackOrStart from "@/components/BackOrStart.vue";

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
      basicData: {
        labels: ['01.01.2022', '01.04.2022', '01.07.2022', '01.09.2022', '01.12.2022'],
        datasets: [
          {
            label: `Регион - ${this.region_id}`,
            data: [0.45, 0.5, 0.56, 0.52, 0.3],
            fill: false,
            borderColor: '#42A5F5',
            tension: .4
          },
        ]
      },
    }
  },
  methods: {
    async selected_bar(e) {
      await this.$router.push({name: 'sector_id_region_id_area_id_table_id', params: {id: this.id, table_id: e.element.index}})
    },
    update_date_range_params() {
      console.log(this.date_range)
    }
  },
}
</script>

<style scoped>

</style>