import { createRouter, createWebHistory } from 'vue-router'
import Top from '@/views/pages/TopPage/MainPage.vue'
import Home from '@/views/pages/HomePage/MainPage.vue'

const routes = [
    { path: '/top', name: 'Top', component: Top },
    { path: '/home', name: 'Home', component: Home },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router