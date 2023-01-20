import axios from "@/plugins/axios"

export default {
    state: {
        map_area_data: []
    },
    actions: {
        async fetch_map_area_data(context, params) {
            const table = await axios.get(`/api/map/area-data/`, {params})
            context.commit('basic', {key: 'area_table_data', value: table.data})
            return table.data
        },
    }
}