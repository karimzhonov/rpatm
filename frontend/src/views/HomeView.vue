<template>
<div v-if="loading" class="layout-main row justify-content-center">
        <div class="col">
                    <ProgressSpinner style="top:30%; left:47%"/>
                </div>
  </div>
  <div v-if="!loading">
  <div class="card rounded-4">
    <h1 class="home-main-header mb-2">{{ $t("индекс человеческого достоинства") }}</h1>
  </div>
  <div class="card rounded-4">
    <h2 class="text-center mb-3">По секторам</h2>
    <div class="grid row justify-content-around">
      <div class="col-3" v-for="item in sector_tables" :key="item.id">
        <div class="pb-2 guide-hover rounded-3">
          <router-link :to="{name: 'sector_id_region', params: {sector_id: item.sector.id}, query: $route.query}"
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
      file: this.$route.query.file,
    })
    await store.dispatch('fetch_region_tables', {file: this.$route.query.file, chart: 'bar'})
    store.commit('basic', {key: 'loading', value: false})
  },
  methods: {
    async selected_bar(e) {
      const region = await store.dispatch('search_region', store.state.region_bar_chart_labels[e.element.index])
      await this.$router.push({
        name: 'region_id_sector', params: {
          region_id: region.id,
        }, query: this.$route.query
      })
    },
  },
  computed: {
    sector_tables: () => store.state.sector_tables,
    barData: () => {
        return {
            labels: store.state.region_bar_chart_labels,
            datasets: store.state.region_bar_chart_data
        }
    },
    loading: () => store.state.loading,
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