import {createStore} from "vuex";
import locale from "@/store/locale";
import auth from "@/store/auth";
import message from "@/store/message";
import sidebar from "@/store/sidebar";
import sector from "@/store/sector";
import region from "@/store/region";
import criteria from "@/store/criteria";
import area from "@/store/area"
import axios from "@/plugins/axios";

export default createStore({
    state: {files: [], data: [], selectedFiles: []},
    getters: {},
    mutations: {
        basic(state, {key, value}) {
            state[key] = value;
        },
        add_main_data(state, data) {
            state.data.push(data)
        },
    },
    actions: {
        get_random_color() {
            return "#" + ((1 << 24) * Math.random() | 0).toString(16).padStart(6, "0")
        },
        async fetch_main_data(context, params) {
            const data = await axios.get('/api/ichd/data-table/', {params})
            context.commit('add_main_data', data.data)
            return data.data
        },
        async fetch_upload_files(context, params = {}) {
            const table = await axios.get('/api/ichd/uploads/', {params})
            context.commit('basic', {key: 'files', value: table.data})
            context.commit('basic', {key: 'selectedFiles', value: [table.data[0]]})
            return table.data
        }
    },
    modules: {
        locale,
        auth,
        message,
        sidebar,
        sector,
        region,
        criteria,
        area,
    },
});
