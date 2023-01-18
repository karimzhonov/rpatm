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
    ]
}]
