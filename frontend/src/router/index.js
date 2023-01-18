import {createRouter, createWebHistory} from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';
import ichd from './ichd';
import passport from './passport';
const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '/',
                    name: 'home',
                    component: () => import('@/views/HomeView.vue')
                },
                ...ichd,
                ...passport,
            ]
        },

        {
            path: '/auth/login',
            name: 'login',
            component: () => import('@/views/Login.vue')
        },
    ]
});

export default router;
