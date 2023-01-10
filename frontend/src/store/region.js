import axios from "@/plugins/axios";

export default {
    state: {
        regions: [],
        region_sectors: [],
        region: {},
        region_line_chart_data: [],
        region_line_chart_labels: [],
        selectedRegionCriteria: [],
        region_bar_chart_data: [],
        region_bar_chart_labels: [],
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
        async fetch_region_tables(context, params = {}) {
            const tables = await axios.get('/api/ichd/region-table/', {params})
            if (params.chart == 'line') {
                const sector_line_chart_labels = []
                const criteria_data = {}
                for (let row of tables.data) {
                    sector_line_chart_labels.push(row.file.date)
                    for (let criteria of row.criteria) {
                        if (criteria_data[criteria.criteria.name]) {
                            criteria_data[criteria.criteria.name].data.push(criteria.index)
                        } else {
                            let color = await context.dispatch('get_random_color')
                            if (criteria.criteria.color) {
                                color = `#${criteria.criteria.color}`
                            }
                            criteria_data[criteria.criteria.name] = {
                                label: criteria.criteria.name,
                                data: [criteria.index],
                                fill: false,
                                borderColor: color,
                                tension: .4
                            }
                        }
                    }
                }
                context.commit('basic', {key: 'selectedRegionCriteria', value: [Object.values(criteria_data)[0]]})
                context.commit('basic', {key: 'region_line_chart_data', value: Object.values(criteria_data)})
                context.commit('basic', {key: 'region_line_chart_labels', value: sector_line_chart_labels})
            } else {
                const datasets = []
                const region_list = []
                let file_name = null
                const data = []
                for (let row of tables.data) {
                    if (!file_name) {
                        file_name = row.file.name
                    }
                    if (!region_list.includes(row.region.name)) {
                        region_list.push(row.region.name)
                    }
                    data.push(row.index)
                }
                datasets.push({
                        label: file_name,
                        data: data,
                        backgroundColor: await context.dispatch('get_random_color'),
                    })
//                context.commit('basic', {key: 'selectedAreaCriteria', value: [files[0]]})
//                context.commit('basic', {key: 'files', value: files})
                context.commit('basic', {key: 'region_bar_chart_data', value: datasets})
                context.commit('basic', {key: 'region_bar_chart_labels', value: region_list})
            }
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
                            let color = await context.dispatch('get_random_color')
                            if (criteria.criteria.color) {
                                color = `#${criteria.criteria.color}`
                            }
                            criteria_data[criteria.criteria.name] = {
                                label: criteria.criteria.name,
                                data: [criteria.index],
                                fill: false,
                                borderColor: color,
                                tension: .4
                            }
                        }
                    }
                }
                context.commit('basic', {key: 'selectedRegionCriteria', value: [Object.values(criteria_data)[0]]})
                context.commit('basic', {key: 'region_line_chart_data', value: Object.values(criteria_data)})
                context.commit('basic', {key: 'region_line_chart_labels', value: sector_line_chart_labels})
            }
            context.commit('basic', {key: 'region_sectors', value: tables.data})
            return tables.data
        },
        async fetch_region(context, id) {
            const region = await axios.get(`/api/ichd/region/${id}/`)
            context.commit('basic', {key: 'region', value: region.data})
            return region
        },
        async search_region(context, search) {
            const regions = await axios.get('/api/ichd/region/', {
                params: {
                    search: search
                }
            })
            return regions.data[0]
        }
    },

}