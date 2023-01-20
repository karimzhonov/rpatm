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
import {i18n} from '@/main'

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
      const {t} = i18n.global
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
      const overlays = {};
      overlays[`<span class="user-select-none" style="font-size: 1rem">${t('Индекс человеческого достоинства')}</span>`] = area_data_layer
      overlays[`<span class="user-select-none" style="font-size: 1rem">${t('Гипермаркеты, магазины')}</span>`] = await this.get_shop_layer()
      overlays[`<span class="user-select-none" style="font-size: 1rem">${t('Аптеки')}</span>`] = await this.get_apteka_layer()
      L.control.layers({}, overlays).addTo(map);
      // Delete Leaflet link
      map.attributionControl.setPrefix('')
    },
    async get_shop_layer() {
      const icon = L.icon({
        iconUrl: '/maps/icons/shop.png',
        iconSize:     [38, 60], // size of the icon
        iconAnchor:   [22, 60], // point of the icon which will correspond to marker's location
        popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
      })

      const r = await fetch('/maps/shop.geojson')
      const data = await r.json()
      const markers = []
      for (let point of data.features) {
        let marker = L.marker([point.properties.y, point.properties.x], {icon}).bindPopup(`<h4 class="text-center">${point.properties.name}</h4>`)
        markers.push(marker)
      }
      return L.layerGroup(markers)
    },
    async get_apteka_layer(){
      const icon = L.icon({
        iconUrl: '/maps/icons/apteka.png',
        iconSize:     [38, 60], // size of the icon
        iconAnchor:   [22, 60], // point of the icon which will correspond to marker's location
        popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
      })

      const r = await fetch('/maps/apteka.geojson')
      const data = await r.json()
      const markers = []
      for (let point of data.features) {
        let marker = L.marker([point.properties.y, point.properties.x], {icon}).bindPopup(`<h4 class="text-center">${point.properties.name}</h4>`)
        markers.push(marker)
      }
      return L.layerGroup(markers)
    },  
    async get_ichd_layer() {
      const {t} = i18n.global
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
            let criteria_html = []
            for (let c of area.criteria) {
              criteria_html.push(`<p>${t(c.criteria)}: <b>${c.index}</b></p>`)
            }
            info_div.innerHTML = `
            <p class="text-center" style="font-size: 1.5rem">${area.area.name}</p>
            <p>${t('Индекс человеческого достоинства')}: <b>${area.index}</b> (${area.delta_index})</p>
            ${criteria_html.join('\n')}
            `
          }
        } else {
          info_div.innerHTML = `
            <p class="text-center">${t('Выберите махаллю')}</p>`
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
                  opacity: 1,
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