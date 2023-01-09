<template>
  <Chart :options="chartOption" :data="chartData" type="radar"/>
</template>

<script>
export default {
  name: "Radar",
  props: ['values', 'labels'],
  data() {
    const values = this.values ? this.values : []
    const datasets = []
    for (let value of values) {
      const color = value.color
      datasets.push(
          {
            label: value.label,
            backgroundColor: `rgba(${color},0.2)`,
            borderColor: `rgba(${color},1)`,
            pointBackgroundColor: `rgba(${color},1)`,
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: `rgba(${color},1)`,
            data: value.data
          },
      )
    }

    return {
      chartData: {
        labels: this.labels,
        datasets: datasets
      },
      chartOption: {
        plugins: {
          legend: {
            labels: {
              color: '#495057'
            }
          }
        },
        scales: {
          r: {
            pointLabels: {
              color: '#495057',
            },
            grid: {
              color: '#ebedef',
            },
            angleLines: {
              color: '#ebedef'
            }
          }
        }
      }
    }
  },
  methods: {
    random_rgba() {
      let o = Math.round, r = Math.random, s = 255;
      return [o(r() * s), o(r() * s), o(r() * s)].join(',')
    }
  }
}
</script>

<style scoped>

</style>