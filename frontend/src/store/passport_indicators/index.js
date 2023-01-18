import axios from "@/plugins/axios";

export default {
    state: {
        selected_files: {}, selected_file: {}, top_bar_years: [],
    },
    actions: {
        async fetch_top_bar_files_passport(context) {
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
    }
}