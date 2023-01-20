<template>
  <div class="card rounded-4">
    <div v-if="loading_map" class="layout-main row justify-content-center" style="width: 100%; height: 85vh">
      <div class="col">
          <ProgressSpinner style="top:40%; left:47%"/>
      </div>
    </div>
    <div v-if="!loading_map" style="width: 100%; height: 85vh">
      <div id="map" style="width: 100%; height: 100%"></div>
    </div>
  </div>
</template>

<script>
import store from "@/store";
import L from "leaflet"

export default {
  name: "HomeView",
  data() {
    return {
      loading_map: true
    }
  }, 
  async mounted() {
    if (this.$route.name == 'home') {
      await this.init_map()
    }
  },
  methods: {
    async init_map() {
      const area_data_layer = await this.get_ichd_layer()
      const map = L.map('map', {
        center: [41.3018622, 69.2684895],
        zoom: 12,
        layers: [area_data_layer], // default layers
        minZoom: 12,
        zoomControl: false,
      })
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
      }).addTo(map);

      // add overlays
      const overlays = {
        'Индекс человеческого достоинства': area_data_layer
      };
      L.control.layers({}, overlays).addTo(map);
      // Delete Leaflet link
      map.attributionControl.setPrefix('')
    },
    async get_ichd_layer() {
      // Fetch data
      const area_table = await store.dispatch('fetch_map_area_data', {file: 0})
      this.loading_map = false
      const area_dict = {}
      for (let area of area_table) {
        area_dict[area.area.global_id] = area
      }
      const r = await fetch('/maps/geodata.json')
      // Info panel
      const info = L.control({position: 'topleft'});
      const info_div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
      info.onAdd = function (map) {
          this.update();
          return info_div;
      };
      info.update = function (props) {
        if (props) {
          const area = area_dict[props.area_id]
          if (area) {
            info_div.innerHTML = `
            <h5>Индекс человеческого достоинства</h5>
            <p class="text-center" style="font-size: 1.5rem">${area.area.name}</p>`
          }
        } else {
          info_div.innerHTML = `
            <h5>Индекс человеческого достоинства</h5>
            <p class="text-center">Выберите махаллю</p>`
        }        
      };
      // Create layer
      const geojson = L.geoJSON(await r.json(), {
        style: function (feature) {
          // set style
          const all_colors = ["#EE391F", "#EE391F", "#EE391F", "#EE391F", "#EE391F", "#FAA10B", "#FAB807", "#F1E000", "#A4D12A", "#27B973"]
          const area = area_dict[feature.properties.area_id]
          if (area) {
            return {
                  fillColor: all_colors[Math.round(area.index * 10) - 1],
                  weight: 2,
                  opacity: 0.5,
                  color: 'white',
                  dashArray: '3',
                  fillOpacity: 0.7,
              };
          }
        },
        onEachFeature: async function (feature, layer) {
          //events
          const area = area_dict[feature.properties.area_id]
          if (area) {            
            layer.on({
              mouseover: (e) => {
                var layer = e.target;
                // Hover effect
                layer.setStyle({
                    weight: 5,
                    color: '#666',
                    dashArray: '',
                    fillOpacity: 0.7
                });
                layer.bringToFront();
                // ToolTip
                layer.bindTooltip(`
                <div>
                  <h4>${area.area.name}</h4>
                </div>`, {direction: 'top'});
              },
              mouseout: (e) => {
                geojson.resetStyle(e.target);
              },
              click: (e) => {
                var layer = e.target;
                info.update(layer.feature.properties);
              }
            })
          }
        }
      }) 
      geojson.onAdd = (map) => {
        geojson.eachLayer(map.addLayer, map);
        info.addTo(map)
      }
      geojson.onRemove = (map) => {
        geojson.eachLayer(map.removeLayer, map);
        info.remove()
      }
      return geojson
    }
  }
}
</script>

<style>
.info {
    padding: 6px 8px;
    font: 14px/16px Arial, Helvetica, sans-serif;
    background: white;
    background: rgba(255,255,255,0.8);
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    border-radius: 5px;
}
.info h4 {
    margin: 0 0 5px;
    color: #777;
}
path.leaflet-interactive:focus {
    outline: none !important;
}
</style>