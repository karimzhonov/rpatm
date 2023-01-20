import {createRouter, createWebHistory} from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';
import ichd from './ichd';
import passport from './passport';
const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/:lang',
            component: AppLayout,
            props: true,
            children: [
                {
                    path: '/:lang',
                    name: 'home',
                    component: () => import('@/views/HomeView.vue'),
                    props: true
                },
                {
                    path: '/:lang/auth/login',
                    name: 'login',
                    component: () => import('@/views/Login.vue'),
                    props: true
                },
                ...ichd,
                ...passport,
            ]
        },
    ]
});

export default router;
