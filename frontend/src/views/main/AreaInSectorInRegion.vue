<template>
  <div class="grid row m-3 justify-content-around">
    <div class="card mt-3 rounded-4">
      <h2 class="text-center">Махалла - {{ area_id }}</h2>
      <div class="col-12">
        <MultiSelect
            :showToggleAll="false"
            v-model="selected"
            :options="options" optionLabel="label"
            placeholder="Select date"
            @change="key += 1"
            style="width:100%"
            class="mb-3"
        />
        <div class="row">
          <div class="col-12">
            <Chart :key="key" type="bar" :data="basicData" :options="basicOptions"
                   @select="selected_bar"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AreaInSectorInRegion",
  props: ['region_id', 'sector_id', 'area_id'],
  data() {
    const labels = [
      'Инсон қадри индекси',
      'Демография', 'Согликни саклаш',
      'Таълим', 'Хавфсизлик', 'Бандлик',
      'Даромад', 'Харакатчанлик', 'Ижтимоий - иктисодий баркарорлик'
    ]
    const radars = [
      {
        id: 1,
        label: '01.12.2022',
        data: [0.556, 0.659, 0.413, 0.186, 0.925, 0.829, 0.440, 0.572, 0.708],
        color: '179,181,198',
        backgroundColor: '#42A5F5',
      },
      {
        id: 2,
        label: '01.11.2022',
        data: [0.526, 0.699, 0.453, 0.286, 0.725, 0.729, 0.490, 0.472, 0.508],
        color: '255,99,132',
        backgroundColor: '#FFA726',
      }
    ]
    return {
      key: 1,
      selected: [radars[0]],
      options: radars,
      labels,
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
      await this.$router.push({
        name: 'sector_id_region_id_area_id_table_id', params: {
          sector_id: this.sector_id, table_id: e.element.index,
          region_id: this.region_id, area_id: this.area_id,
        }
      })
    },
  },
  computed: {
    radarData() {
      return this.selected
    },
    basicData() {
      return {
        labels: this.labels,
        datasets: this.selected
      }
    },
  }
}
</script>

<style scoped>

</style>