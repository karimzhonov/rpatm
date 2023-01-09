<template>
  <div class="card rounded-4">
    <h1 class="home-main-header mb-2">{{ $t("home.header") }}</h1>
  </div>
  <div class="card rounded-4">
    <h2 class="text-center mb-3">По секторам</h2>
    <div class="grid row justify-content-around">
      <div class="col-3" v-for="item in sector_tables" :key="item.id">
        <div class="pb-2 guide-hover rounded-3">
          <router-link :to="{name: 'sector_id_region', params: {sector_id: item.sector.id}}"
                       class="text-decoration-none speedometer-label">
            <speedometer :value="item.index" :label="`${$t('Сектор')} - ${item.sector.number }`" :delta_index="item.delta_index"/>
          </router-link>
        </div>
      </div>
    </div>
  </div>
  <div class="card rounded-4">
    <h2 class="text-center mb-3">По районам</h2>
    <Chart type="bar" :data="barData" :options="barOptions" @select="selected_bar"/>
  </div>

</template>

<script>
import Speedometer from "@/components/Speedometer.vue";
import store from "@/store";

export default {
  name: "HomeView",
  components: {Speedometer},
  data() {
    return {
      barData: {
        labels: ['Tuman - 1', 'Tuman - 2', 'Tuman - 3', 'Tuman - 4', 'Tuman - 5', 'Tuman - 6', 'Tuman - 7'],
        datasets: [
          {
            label: '01.01.2023',
            backgroundColor: '#42A5F5',
            data: [65, 59, 80, 81, 56, 55, 40]
          },
        ]
      },
      barOptions: {
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
    await store.dispatch('fetch_sector_tables', {
      file: 0
    })
  },
  methods: {
    async selected_bar(e) {
      await this.$router.push({
        name: 'region_id_sector', params: {
          region_id: e.element.index,
        }
      })
    },
  },
  computed: {
    sector_tables: () => store.state.sector_tables
  }
}
</script>

<style>

.home-main-header {
  margin-bottom: 5rem;
  font-size: 3rem;
  text-transform: uppercase;
  text-align: center;
}

.guide-hover:hover {
  box-shadow: 1px 1px 3px 3px #CCCCCC;
}
</style>