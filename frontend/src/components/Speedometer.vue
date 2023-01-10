<template>
  <div>
    <div class="row justify-content-end">
      <div v-if="delta_index > 0" class="col-4 text-center" style="color: green">+{{ delta_index }}</div>
      <div v-if="delta_index < 0" class="col-4 text-center" style="color: red">{{ delta_index }}</div>
      <div v-if="delta_index === 0" class="col-4 text-center">{{ delta_index }}</div>
    </div>
    <div class="text-center" style="font-size: 2rem">
      {{label}}
    </div>
    <vue-apex-charts type="radialBar" :options="chartOptions" :series="series"/>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: "Speedometer",
  props: ['value', 'label', 'delta_index'],
  data() {
    return {
      series: [this.value * 100],
      chartOptions: {
        chart: {
          type: 'radialBar',
          offsetY: -20,
          sparkline: {
            enabled: true
          },
        },
        colors: [this.rgbToHex(...this.get_color())],
        plotOptions: {
          radialBar: {
            startAngle: -90,
            endAngle: 90,
            maxValue: 1,
            track: {
              background: "#e7e7e7",
              strokeWidth: '97%',
              margin: 5, // margin is in pixels
              dropShadow: {
                enabled: true,
                top: 2,
                left: 0,
                color: '#999',
                opacity: 1,
                blur: 2
              }
            },
            dataLabels: {
              name: {
                show: false
              },
              value: {
                formatter: function (val) {
                    let value = Math.round(val * 10) / 1000
                    value = `${value}000000`
                  return value.slice(0, 5);
                },
                offsetY: -2,
                fontSize: '22px'
              }
            }
          }
        },
        grid: {
          padding: {
            top: -10
          }
        },

        fill: {
          type: 'gradient',
          gradient: {
            shade: 'light',
            shadeIntensity: 0.4,
            inverseColors: false,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 50, 53, 91]
          },
        },
        labels: ['Average Results'],
      },
    }
  },
  components: {VueApexCharts},
  methods: {
    rgbToHex(r, g, b) {
      return "#" + (1 << 24 | r << 16 | g << 8 | b).toString(16).slice(1);
    },
    get_color() {
      const colors = {
        r: [
          {
            value: 255,
            range: [0, 0.399],
          },
          {
            value: 241,
            range: [0.4, 0.449],
          },
          {
            value: 255,
            range: [0.45, 0.499],
          },
          {
            value: 254,
            range: [0.5, 0.549],
          },
          {
            value: 118,
            range: [0.550, 0.599],
          },
          {
            value: 116,
            range: [0.6, 0.649],
          },
          {
            value: 113,
            range: [0.65, 0.699],
          },
          {
            value: 131,
            range: [0.7, 0.749],
          },
          {
            value: 109,
            range: [0.75, 0.799],
          },
          {
            value: 121,
            range: [0.8, 0.849],
          },
          {
            value: 109,
            range: [0.85, 0.899],
          },
          {
            value: 91,
            range: [0.9, 2],
          },
        ],
        g: [
          {
            value: 114,
            range: [0, 0.399],
          },
          {
            value: 255,
            range: [0.4, 0.449],
          },
          {
            value: 210,
            range: [0.45, 0.499],
          },
          {
            value: 178,
            range: [0.5, 0.549],
          },
          {
            value: 167,
            range: [0.55, 0.599],
          },
          {
            value: 177,
            range: [0.6, 0.649],
          },
          {
            value: 216,
            range: [0.65, 0.699],
          },
          {
            value: 241,
            range: [0.7, 0.749],
          },
          {
            value: 255,
            range: [0.75, 0.799],
          },
          {
            value: 252,
            range: [0.8, 0.849],
          },
          {
            value: 225,
            range: [0.85, 0.899],
          },
          {
            value: 174,
            range: [0.9, 2],
          },
        ],
        b: [
          {
            value: 113,
            range: [0, 0.399],
          },
          {
            value: 197,
            range: [0.4, 0.449],
          },
          {
            value: 255,
            range: [0.449, 0.499],
          },
          {
            value: 120,
            range: [0.5, 0.549],
          },
          {
            value: 251,
            range: [0.55, 0.599],
          },
          {
            value: 255,
            range: [0.6, 0.649],
          },
          {
            value: 255,
            range: [0.65, 0.699],
          },
          {
            value: 248,
            range: [0.7, 0.749],
          },
          {
            value: 250,
            range: [0.75, 0.799],
          },
          {
            value: 120,
            range: [0.8, 0.849],
          },
          {
            value: 107,
            range: [0.85, 0.899],
          },
          {
            value: 92,
            range: [0.9, 2],
          },
        ]
      }
      return [this._get_color_com(colors.r), this._get_color_com(colors.g), this._get_color_com(colors.b)]
    },
    _get_color_com(c) {
      for (let cc of c) {
        if (cc.range[0] <= this.value && this.value <= cc.range[1]) {
          return cc.value
        }
      }
    },
  }
}
</script>

<style scoped>

</style>