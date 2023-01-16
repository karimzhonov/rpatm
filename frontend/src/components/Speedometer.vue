<template>
    <div class="row justify-content-end" style="color: var(--surface-900)!important;">
      <div v-if="delta_index > 0" class="col-4 p-0 text-center" style="color: green">+{{ delta_index }}</div>
      <div v-if="delta_index < 0" class="col-4 p-0 text-center" style="color: red">{{ delta_index }}</div>
      <div v-if="delta_index === 0" class="col-4 p-0 text-center"></div>
    </div>
    <h4 class="text-center pb-3" style="font-size: 2rem">
      {{label}}
    </h4>
    <vue-gauge :refid="`a-${get_random_str()}`" :options="guageOptions"></vue-gauge>
    <p class="text-center position-relative" style="top: -50px; font-size: 1.5rem; color: var(--surface-900)!important;">{{ format_value(value * 100) }}</p>
</template>

<script>
import VueGauge from 'vue-gauge';

export default {
  name: "Speedometer",
  props: ['value', 'label', 'delta_index', 'id'],
  data() {
    return {
      guageOptions: {
        needleValue: this.value * 100,
        arcColors: ["#EE391F", "#F45318", "#F77612", "#F9920D", "#FBAC09", "#FAB807", "#F6E200", "#F1E000", "#A4D12A", "#27B973"],
        arcLabels: ["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"],
        arcDelimiters:[10,20, 30, 40, 50, 60, 70, 80, 90],
        hasNeedle: true,
        rangeLabel: ['0', '1.0'],
        needleColor: "#000000",
        chartWidth: 330,
        needleColor: 'var(--surface-900)'
      }
    }
  },
  components: {VueGauge},
  methods: {
  format_value(val) {
    let value = Math.round(val * 10) / 1000
        value = `${value}000000`
      return value.slice(0, 5);
    },
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
    get_random_str() {
      let result           = '';
      let characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      let charactersLength = characters.length;
      for ( let i = 0; i < 7; i++ ) {
          result += characters.charAt(Math.floor(Math.random() * charactersLength));
      }
      return result;
    }
  }
}
</script>

<style scoped>

</style>