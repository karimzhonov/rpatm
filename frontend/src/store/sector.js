import axios from "@/plugins/axios";

export default {
    state: {
        sector: {},
        sectors: [],
        sector_tables: [],
        sector_line_chart_data: [],
        sector_line_chart_labels: [],
        selectedSectorCriteria: [],
    },
    actions: {
        async fetch_sector(context, id) {
            const sectors = await axios.get(`/api/ichd/sector/${id}`)
            context.commit('basic', {key: 'sector', value: sectors.data})
            return sectors.data
        },
        async fetch_sectors(context, params = {}) {
            if (context.state.sectors.length > 0) {
                return context.state.sectors
            }
            const sectors = await axios.get('/api/ichd/sector/', {params})
            context.commit('basic', {key: 'sectors', value: sectors.data})
            return sectors.data
        },
        async fetch_sector_tables(context, params = {}) {
            const tables = await axios.get('/api/ichd/sector-table/', {params})
            if (tables.data.length > 0) {
                const sector_line_chart_labels = []
                const criteria_data = {}
                for (let row of tables.data) {
                    sector_line_chart_labels.push(row.file.date)
                    for (let criteria of row.criteria) {
                        if (criteria_data[criteria.criteria.name]) {
                            criteria_data[criteria.criteria.name].data.push(criteria.index)
                        } else {
                            criteria_data[criteria.criteria.name] = {
                                label: criteria.criteria.name,
                                data: [criteria.index],
                                fill: false,
                                borderColor: criteria.color ?? await context.dispatch('get_random_color'),
                                tension: .4
                            }
                        }
                    }
                }
                context.commit('basic', {key: 'selectedSectorCriteria', value: [Object.values(criteria_data)[0]]})
                context.commit('basic', {key: 'sector_line_chart_data', value: Object.values(criteria_data)})
                context.commit('basic', {key: 'sector_line_chart_labels', value: sector_line_chart_labels})
            } else {
                context.commit('basic', {key: 'sector_line_chart_data', value: []})
                context.commit('basic', {key: 'sector_line_chart_labels', value: []})
            }
            context.commit('basic', {key: 'sector_tables', value: tables.data})
            return tables.data
        },

    }
}