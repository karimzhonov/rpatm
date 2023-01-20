export default [{
    path: "/ichd",
    component: () => import("@/views/ichd/ICHDLayout.vue"),
    children: 
    [
        {
            path: '/:lang/ichd',
            name: 'ichd_main',
            component: () => import('@/views/ichd/Main.vue')
        },
        {
            path: '/:lang/ichd/sector/:sector_id/region/:region_id',
            name: 'ichd_sector_id_region_id',
            component: () => import('@/views/ichd/SectorRegion.vue'),
            props: true
        },
    
        {
            path: '/:lang/ichd/sector/:sector_id/region/:region_id/criteria/:criteria_id',
            name: 'ichd_sector_id_region_id_criteria_id',
            component: () => import('@/views/ichd/AreaTable.vue'),
            props: true
        },
    
        {
            path: '/:lang/ichd/data-table',
            name: 'ichd_data_table',
            component: () => import('@/views/ichd/DataTable.vue')
        },
    
        {
            path: '/:lang/ichd/region',
            name: 'ichd_region',
            component: () => import('@/views/ichd/RegionBar.vue')
        },
    
        {
            path: '/:lang/ichd/region-data',
            name: 'ichd_region-data-table',
            component: () => import('@/views/ichd/RegionTable.vue')
        },
    
        {
            path: '/:lang/ichd/area-data-table',
            name: 'ichd_area-data-table',
            component: () => import('@/views/ichd/AreaDataTable.vue')
        },
    
        {
            path: '/:lang/ichd/sector/:sector_id/region',
            name: 'sector_id_region',
            component: () => import('@/views/ichd/Sector.vue'),
            props: true,
        },
        {
            path: '/:lang/ichd/sector/:sector_id/region/:region_id/area',
            name: 'sector_id_region_id_area',
            component: () => import('@/views/ichd/RegionInSector.vue'),
            props: true
        },
        {
            path: '/:lang/ichd/sector/:sector_id/region/:region_id/area/:area_id',
            name: 'sector_id_region_id_area_id',
            component: () => import('@/views/ichd/AreaInRegionInSector.vue'),
            props: true,
        },
        {
            path: '/:lang/ichd/sector/:sector_id/region/:region_id/area/:area_id/criteria/:criteria_id',
            name: 'sector_id_region_id_area_id_table_id',
            component: () => import('@/views/ichd/TableAreaInRegionInSector.vue'),
            props: true,
        },
    
        {
            path: '/:lang/ichd/region/:region_id/sector',
            name: 'region_id_sector',
            component: () => import('@/views/ichd/Region.vue'),
            props: true
        },
        {
            path: '/:lang/ichd/region/:region_id/sector/:sector_id/area',
            name: 'region_id_sector_id',
            component: () => import('@/views/ichd/SectorInRegion.vue'),
            props: true
        },
    ]
}]
