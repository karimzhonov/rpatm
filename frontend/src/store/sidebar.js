
export default {
    state: {
        sidebar: []
    },
    actions: {
        async fetch_sidebar(context) {
            const menu = []
            const sector_menu = {
                label: 'sidebar.sector.header',
                items: []
            }
            const sectors = await context.dispatch('fetch_sectors')
            for (let sector of sectors) {
                sector_menu.items.push(
                    {
                        label: `Сектор - ${sector.number}`,
                        to: {name: 'sector_id_region', params: {sector_id: sector.id}},
                    }
                )
            }
            const regions = await context.dispatch('fetch_regions')
            const region_menu = {
                label: 'sidebar.region.header',
                items: []
            }
            for (let region of regions) {
                region_menu.items.push(
                    {
                        label: region.name,
                        to: {name: 'region_id_sector', params: {region_id: region.id}}
                    }
                )
            }
            menu.push(sector_menu, region_menu)
            context.commit('set_sidebar', menu)
        }
    },
    getters: {
        get_sidebar: (state) => state.sidebar
    },
    mutations: {
        set_sidebar(state, data) {
            state.sidebar = data
        }
    }
}