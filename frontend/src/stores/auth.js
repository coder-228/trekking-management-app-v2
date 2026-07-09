import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        user: JSON.parse(localStorage.getItem('user')) || null,
        loading: false,
        error: null
    }),

    getters: {
        isAuthenticated: (state) => !!state.token,
        isAdmin: (state) => state.user?.role === 'admin',
        isStaff: (state) => state.user?.role === 'staff',
        isUser: (state) => state.user?.role === 'user',
        userRole: (state) => state.user?.role,
        userName: (state) => state.user?.name
    },

    actions: {
        async login(username, password) {
            this.loading = true
            this.error = null
            try {
                const response = await axios.post('/api/auth/login', {
                    username,
                    password
                })
                this.token = response.data.token
                this.user = response.data.user

                // Persist to localStorage
                localStorage.setItem('token', this.token)
                localStorage.setItem('user', JSON.stringify(this.user))

                return { success: true, role: this.user.role }
            } catch (error) {
                this.error = error.response?.data?.error || 'Login failed'
                return { success: false, error: this.error }
            } finally {
                this.loading = false
            }
        },

        async register(userData) {
            this.loading = true
            this.error = null
            try {
                await axios.post('/api/auth/register', userData)
                return { success: true }
            } catch (error) {
                this.error = error.response?.data?.errors?.join(', ')
                    || error.response?.data?.error
                    || 'Registration failed'
                return { success: false, error: this.error }
            } finally {
                this.loading = false
            }
        },

        logout() {
            this.token = null
            this.user = null
            localStorage.removeItem('token')
            localStorage.removeItem('user')
        }
    }
})
