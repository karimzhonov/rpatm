<template>
<div v-if="loading" class="layout-main row justify-content-center">
    <div class="col">
        <ProgressSpinner style="top:30%; left:47%"/>
    </div>
</div>
<div v-if="!loading">
  <div class="row">
    <div class="col-12 row p-3 mb-0 p-0">
        <div>
            <div class="home-main-header mb-1">
                <img style="color: var(--surface-900)" class="mr-2" :src="logo" width="150"/>
                {{ $t("индекс человеческого достоинства") }}
            </div>
        </div>
    </div>
    <h1 class="m-3 text-center">{{ $t('Показатели города') }}</h1>
    <div class="col-12 row p-0">
        <div class="col-3">
            <router-link :to="{name: 'ichd_region', query: {year: $route.query.year, file: $route.query.file}}">
            <div class="card rounded-4" style="padding: 16px" v-tooltip.top="{value: `Нажмите что бы увидеть по районам`, escape: true, class: 'text-center'}">
                <div class="row" style="text-align: center;">
                    <div class="col">
                        <div class="col p-0 text-900 font-medium" style="font-size: 2.5rem">{{home_city_data.criteria[0].index}}</div>
                        <p class="text-center text-500 font-medium" style="font-size: 2rem;">{{home_city_data.criteria[0].criteria.name}}</p>
                    </div>
                </div>
            </div>
            </router-link>
        </div>
        <div class="col">
            <router-link :to="{name: 'ichd_data_table', query: {file: $route.query.file, year: $route.query.year, index_color:'red'}}">
                <div class="card rounded-4">
                    <div style="text-align: center;">
                        <div class="row justify-content-center mb-1 pr-4 align-items-center">
                            <div class="col p-0 text-900 font-medium text-xl">
                                <p class="text-center text-500 font-medium mb-0">{{ $t('Махалли с низким индексом') }}</p> 
                                <p style="font-size: 2rem">{{ home_city_data.area_info.min_count }}</p>
                            </div>
                            <div class="flex align-items-center justify-content-center border-round" style="width:4rem;height:4rem">
                                <font-awesome-icon icon="fa-regular fa-face-frown" style="font-size: 3rem;" class="text-red-500"/>
                            </div>
                        </div>
                    </div>
                </div>
            </router-link>
        </div>
        <div class="col">
            <router-link :to="{name: 'ichd_data_table', query: {file: $route.query.file, year: $route.query.year, index_color:'blue'}}">
            <div class="card rounded-4">
                <div style="text-align: center;">
                    <div class="row justify-content-center mb-1 pr-4 align-items-center">
                        <div class="col p-0 text-900 font-medium text-xl">
                            <p class="text-center text-500 font-medium mb-0">{{ $t('Махалли со средним индексом') }}</p> 
                            <p style="font-size: 2rem">{{ home_city_data.area_info.center_count }}</p>
                        </div>
                        <div class="flex align-items-center justify-content-center border-round" style="width:4rem;height:4rem">
                            <font-awesome-icon icon="fa-regular fa-face-meh" style="font-size: 3rem;" class="text-blue-500"/>
                        </div>
                    </div>
                </div>
            </div>
        </router-link>
        </div>
        <div class="col">
            <router-link :to="{name: 'ichd_data_table', query: {file: $route.query.file, year: $route.query.year, index_color:'green'}}">
            <div class="card rounded-4">
                <div style="text-align: center;">
                    <div class="row justify-content-center mb-1 pr-4 align-items-center">
                        <div class="col p-0 text-900 font-medium text-xl">
                            <p class="text-center text-500 font-medium mb-0">{{ $t('Махалли с высоким индексом') }}</p> 
                            <p style="font-size: 2rem">{{ home_city_data.area_info.max_count }}</p>
                        </div>
                        <div class="flex align-items-center justify-content-center border-round" style="width:4rem;height:4rem">
                            <font-awesome-icon icon="fa-regular fa-face-smile" style="font-size: 3rem;" class="text-green-500"/>
                        </div>
                    </div>
                </div>
            </div>
        </router-link>
        </div>
        <div></div>
    </div>

    <div class="col-12 row p-0">
        <div class="card col mb-2 rounded-4 ml-3 mr-3" v-for="(item, i) in home_city_data.criteria.slice(1, 9)" :key="item">
            <router-link :to="{name: 'ichd_region-data-table', query: {file: $route.query.file, year: $route.query.year, criteria: item.criteria.id}}">
            <div style="text-align: center;">
                <div class="row justify-content-center mb-1">
                    <div class="flex align-items-center justify-content-center border-round mb-1" style="width:3rem;height:3rem">
                        <font-awesome-icon :icon="icons[i]" style="font-size: 3rem;" :class="icon_bg_color_classes[i]"/>
                    </div>
                </div>
                <div class="col p-0 text-900 font-medium text-xl">{{item.index}}</div>
                <p class="text-center text-500 font-medium">{{item.criteria.name}}</p>
            </div>
            </router-link>
        </div>
        <div></div>
    </div>

        
    </div>
<h1 class="m-3 text-center">{{ $t('Показатели по секторам') }}</h1>

  <div class="grid row justify-content-between">
    <div class="col-12 row pb-0 justify-content-between" v-for="sector in home_sectors_data" :key="sector">
        <div class="col-3 row pt-0">
            <div class="grid row justify-content-around">
                <div class="col-12 card rounded-4 p-0">
                    <div class="pb-2 rounded-3 pt-4">
                        <router-link :to="{name: 'sector_id_region', params: {sector_id: sector.sector.id}, query: $route.query}"
                                    class="text-decoration-none speedometer-label">
                            <speedometer :value="sector.index" :label="`${$t('Сектор')} - ${sector.sector.number }`" :delta_index="sector.delta_index"/>
                        </router-link>
                    </div>
                </div>
                <router-link class="p-0" :to="{name: 'ichd_data_table', query: {file: $route.query.file, year: $route.query.year, index_color:'red', sector: sector.sector.id}}">
                <div class="card p-3 col-12 rounded-4 pb-0">
                    <div style="text-align: center;">
                        <div class="row justify-content-center mb-1 pr-3 pl-3 align-items-center">
                            <div class="col p-0 text-900 font-medium text-xl">
                                <p class="text-center text-500 font-medium">{{ $t('Махалли с низким индексом') }}</p> 
                                <p style="font-size: 1.5rem">{{sector.area_info.min_count ?? 0}}</p>
                            </div>
                            <div class="flex align-items-center justify-content-center border-round" style="width:4rem;height:4rem">
                                <font-awesome-icon icon="fa-regular fa-face-frown" style="font-size: 2.5rem;" class="text-red-500"/>
                            </div>
                        </div>
                    </div>
                </div>
            </router-link>
                <router-link class="p-0" :to="{name: 'ichd_data_table', query: {file: $route.query.file, year: $route.query.year,  index_color:'blue', sector: sector.sector.id}}">
                <div class="card p-3 col-12 rounded-4">
                    <div style="text-align: center;">
                        <div class="row justify-content-center mb-1 pr-3 pl-3 align-items-center">
                            <div class="col p-0 text-900 font-medium text-xl">
                                <p class="text-center text-500 font-medium">{{ $t('Махалли со средним индексом') }}</p> 
                                <p style="font-size: 1.5rem">{{sector.area_info.center_count ?? 0}}</p>
                            </div>
                            <div class="flex align-items-center justify-content-center border-round" style="width:4rem;height:4rem">
                                <font-awesome-icon icon="fa-regular fa-face-meh" style="font-size: 2.5rem;" class="text-blue-500"/>
                            </div>
                        </div>
                    </div>
                </div>
            </router-link>
                <router-link class="p-0" :to="{name: 'ichd_data_table', query: {file: $route.query.file, year: $route.query.year, index_color:'green', sector: sector.sector.id}}">
                <div class="card p-3 col-12 rounded-4">
                    <div style="text-align: center;">
                        <div class="row justify-content-center mb-1 pr-3 pl-3 align-items-center">
                            <div class="col p-0 text-900 font-medium text-xl">
                                <p class="text-center text-500 font-medium">{{ $t('Махалли с высоким индексом') }}</p> 
                                <p style="font-size: 1.5rem">{{sector.area_info.max_count ?? 0}}</p>
                            </div>
                            <div class="flex align-items-center justify-content-center border-round" style="width:4rem;height:4rem">
                                <font-awesome-icon icon="fa-regular fa-face-smile" style="font-size: 2.5rem;" class="text-green-500"/>
                            </div>
                        </div>
                    </div>
                </div>
            </router-link>
            </div>
        </div>

        <div class="col-9 pl-0 pb-0 pr-0">
            <div class="grid">
                <div class="col-12 row pt-0 pl-0 pr-0">
                    <div class="col-12 mb-0 card rounded-4">
                        <Bar :series="sector.bar.datasets" :labels="sector.bar.labels" @dataPointSelection="async (e, chart, config) => await bar_selected(sector.bar.labels[config.dataPointIndex], sector.sector.id)"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>
    
</div>
</template>

<script>
import Speedometer from "@/components/Speedometer.vue";
import store from "@/store";
import Bar from "@/components/Bar.vue";
import logo_light from "@/assets/images/logo minimalis.svg"
import logo_dark from "@/assets/images/logo minimalist light (1).svg"

export default {
  name: "ICHDMainView",
  components: {Speedometer, Bar},
  data() {
    return {
        logo_light, logo_dark,
        icon_bg_color_classes: ['text-blue-300', 'text-green-300', 'text-orange-300', 'text-red-300', 'text-purple-300', 'text-blue-300', 'text-yellow-300', 'text-green-300'],
        icons: ['fa-solid fa-kit-medical', 'fa-solid fa-briefcase', 'fa-solid fa-graduation-cap', 
        'fa-solid fa-wallet', 'fa-solid fa-hands-holding-child', 'fa-solid fa-shield-halved', 'fa-solid fa-building-wheat', 'fa-solid fa-chart-line']
    }
  },
  async mounted() {
    await store.dispatch('fetch_home_city_data', {file: this.$route.query.file})
    await store.dispatch('fetch_home_sectors_data', {file: this.$route.query.file})
    store.commit('basic', {key: 'loading', value: false})
  },
  methods: {
    async bar_selected(region, sector_id) {
        region = await store.dispatch('search_region', region)
        this.$router.push({name: 'ichd_sector_id_region_id', params: {sector_id: sector_id, region_id: region.id}, query: {file: this.$route.query.file, year: this.$route.query.year}})
    },
  },
  computed: {
    home_sectors_data: () => store.state.home_sectors_data,
    loading: () => store.state.loading,
    home_city_data: () => store.state.home_city_data,
    logo() {
        return !store.state.darkMode ? this.logo_light : this.logo_dark
    }
  }
}
</script>

<style>

.home-main-header {
  margin-bottom: 5rem;
  font-size: 2.5rem;
  text-transform: uppercase;
  text-align: center;
  line-height: 70px;
  color: var(--surface-900);
}
</style>