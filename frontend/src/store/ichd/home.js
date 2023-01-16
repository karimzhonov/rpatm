import axios from "@/plugins/axios"

export default {
    state: {home_sectors_data: [], home_city_data: {}},
    actions: {
        async fetch_home_sectors_data(context, params={}){
            const table = await axios.get('/api/ichd/home-sector-chart/', {params})
            context.commit('basic', {key: 'home_sectors_data', value: table.data})
            return table.data
        },
        async fetch_home_city_data(context, params={}) {
            const table = await axios.get('/api/ichd/home-city-data/', {params})
            context.commit('basic', {key: 'home_city_data', value: table.data})
            return table.data
        }
    }
}