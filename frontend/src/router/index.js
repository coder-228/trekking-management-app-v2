import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/LoginView.vue'),
        meta: { guest: true }
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/RegisterView.vue'),
        meta: { guest: true }
    },
    // Admin routes
    {
        path: '/admin',
        meta: { requiresAuth: true, role: 'admin' },
        children: [
            {
                path: 'dashboard',
                name: 'AdminDashboard',
                component: () => import('../views/admin/DashboardView.vue')
            },
            {
                path: 'treks',
                name: 'AdminTreks',
                component: () => import('../views/admin/TreksView.vue')
            },
            {
                path: 'staff',
                name: 'AdminStaff',
                component: () => import('../views/admin/StaffView.vue')
            },
            {
                path: 'users',
                name: 'AdminUsers',
                component: () => import('../views/admin/UsersView.vue')
            },
            {
                path: 'bookings',
                name: 'AdminBookings',
                component: () => import('../views/admin/BookingsView.vue')
            }
        ]
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/login'
 }]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Navigation guard
router.beforeEach((to, from) => {
    const auth = useAuthStore()

    if (to.meta.requiresAuth && !auth.isAuthenticated) {
        return '/login'
    }

    if (to.meta.guest && auth.isAuthenticated) {
        return `/${auth.userRole}/dashboard`
    }

    if (to.meta.role && auth.user?.role !== to.meta.role) {
        return `/${auth.userRole}/dashboard`
    }
})

export default router
