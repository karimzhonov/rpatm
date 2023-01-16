import axios from "@/plugins/axios";

export default {
    state: {
        criteriaChildren: [],
        selectedCriteria: [],
        criteria_list: [],
        criteria: [],
    },
    actions: {
        async fetch_criterias(context, params = {}) {
            const criteria = await axios.get('/api/ichd/criteria/', {params})
            context.commit('basic', {key: 'criteriaChildren', value: criteria.data})
            return criteria.data
        },
        async fetch_criteria(context, id){
            const criteria = await axios.get(`/api/ichd/criteria/${id}`)
            context.commit('basic', {key: 'criteria', value: criteria.data})
            return criteria.data
        },
        async search_criteria(context, item) {
            const criteria = await axios.get('/api/ichd/criteria/', {
                params: {
                    search: item
                }
            })
            return criteria.data[0]
        }
    },
    mutations: {
        add_criteria(state, value) {
            state.selectedCriteria.push(value)
        }
    }
}