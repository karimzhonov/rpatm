export default [{
    path: "/passport",
    component: () => import("@/views/passport_indicators/Layout.vue"),
    children: 
    [
        {
            path: '/passport',
            name: 'passport_main',
            component: () => import('@/views/passport_indicators/Main.vue')
        },
        {
            path: '/passport/region/:region_id',
            name: 'passport_region_data',
            component: () => import('@/views/passport_indicators/RegionData.vue'),
            props: true
        },
    ]
}]
