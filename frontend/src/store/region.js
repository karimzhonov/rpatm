import axios from "@/plugins/axios";

export default {
    state: {
        regions: [],
        region_sectors: [],
        region: {},
        region_line_chart_data: [],
        region_line_chart_labels: [],
        selectedRegionCriteria: [],
    },
    actions: {
        async fetch_regions(context, params) {
            if (context.state.regions.length > 0) {
                return context.state.regions
            }
            const regions = await axios.get('/api/ichd/region/', {params})
            context.commit('basic', {key: 'regions', value: regions.data})
            return regions.data
        },
        async fetch_region_sectors(context, params = {}) {
            const tables = await axios.get('/api/ichd/region-sector-table/', {params})
            if (params.chart) {
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
                console.log(sector_line_chart_labels)
                context.commit('basic', {key: 'selectedRegionCriteria', value: [Object.values(criteria_data)[0]]})
                context.commit('basic', {key: 'region_line_chart_data', value: Object.values(criteria_data)})
                context.commit('basic', {key: 'region_line_chart_labels', value: sector_line_chart_labels})
            }
            context.commit('basic', {key: 'region_sectors', value: tables.data})
            return tables.data
        },
        async fetch_region(context, id) {
            const region = await axios.get(`/api/ichd/region/${id}`)
            context.commit('basic', {key: 'region', value: region.data})
            return region
        },
    },

}