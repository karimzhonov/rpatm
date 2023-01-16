import {createStore} from "vuex";
import locale from "@/store/locale";
import auth from "@/store/auth";
import message from "@/store/message";
import sidebar from "@/store/sidebar";
import sector from "@/store/ichd/sector";
import region from "@/store/ichd/region";
import criteria from "@/store/ichd/criteria";
import area from "@/store/ichd/area"
import ichd_home from "./ichd/home"
import axios from "@/plugins/axios";

export default createStore({
    state: {
        files: [], data: [], selectedFiles: [], loading: true, 
        selected_year: {}, top_bar_years: [], selected_file: {}, city_criteria: [],
        data_table: [],
        darkMode: false,
        messages: [],
    },
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
        async fetch_data_table(context, params) {
            const data = await axios.get('/api/ichd/data-table/', {params})
            context.commit('basic', {key: 'data_table', value: data.data})
            return data.data
        },
        async fetch_upload_files(context, params = {}) {
            const table = await axios.get('/api/ichd/uploads/', {params})
            context.commit('basic', {key: 'files', value: table.data})
            context.commit('basic', {key: 'selectedFiles', value: [context.state.selected_file]})
            return table.data
        },
        async fetch_top_bar_files(context) {
            const table = await axios.get('/api/ichd/uploads/')
            const years = {}
            for (let file of table.data) {
                if (!years[file.date.split('-')[0]]) {
                    years[file.date.split('-')[0]] = {
                        year: file.date.split('-')[0],
                        files: [],
                    }
                }
                years[file.date.split('-')[0]].files.push(file)
            }

            context.commit('basic', {key: 'top_bar_years', value: Object.values(years)})

            const url = new URL(window.location.href)
            if (!url.searchParams.get('year')) {
                url.searchParams.set('year', Object.values(years)[0].year)
            }
            if (!url.searchParams.get('file')) {
                url.searchParams.set('file', Object.values(years)[0].files[0].id)
            }
            let selected_file = {}
            for (let file of years[url.searchParams.get('year')].files) {
                if (file.id == url.searchParams.get('file')) {
                    selected_file = file
                }
            }

            if (window.location.href !== url.href) {
                window.location = url
            }

            context.commit('basic', {key: 'selected_year', value: years[url.searchParams.get('year')]})
            context.commit('basic', {key: 'selected_file', value: selected_file})

            return Object.values(years)
        },
        async fetch_city_table_criteria(context, params={}) {
            const data = await axios.get('/api/ichd/city-criteria-table/', {params})
            context.commit('basic', {key: 'city_criteria', value: data.data})
            return data.data
        },
    },
    modules: {
        ichd_home,
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
