import axios from "@/plugins/axios";

export default {
    state: {
        area: {},
        area_line_chart_data: [],
        area_line_chart_labels: [],
        area_region_sector: [],
        selectedAreaCriteria: [],
        area_table_data: []
    },
    actions: {
        async fetch_area_table_data(context, params) {
            const table = await axios.get(`/api/ichd/area-data/`, {params})
            context.commit('basic', {key: 'area_table_data', value: table.data})
            return table.data
        },
        async fetch_area(context, id) {
            const area = await axios.get(`/api/ichd/area/${id}/`)
            context.commit('basic', {key: 'area', value: area.data})
            return area.data
        },
        async fetch_area_region_sector(context, params = {}) {
            const tables = await axios.get('/api/ichd/area-table/', {params})
            if (params.chart) {
                const files = []
                const datasets = []
                const criteria_list = []

                for (let row of tables.data) {
                    files.push(row.file)
                    const data = []
                    for (let c of row.criteria) {
                        if (!criteria_list.includes(c.criteria.name)) {
                            criteria_list.push(c.criteria.name)
                        }
                        data.push(c.index)
                    }
                    datasets.push({
                        name: row.file.name,
                        data: data,
                    })
                }
//                context.commit('basic', {key: 'selectedAreaCriteria', value: [files[0]]})
//                context.commit('basic', {key: 'files', value: files})
                context.commit('basic', {key: 'area_line_chart_data', value: datasets})
                context.commit('basic', {key: 'area_line_chart_labels', value: criteria_list})
            }
            context.commit('basic', {key: 'area_region_sector', value: tables.data})
            return tables.data
        },
    }
}