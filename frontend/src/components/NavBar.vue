<template>
  <nav class="navbar">
    <div class="nav-brand">
      <span class="nav-icon">▲</span>
      Summit<span class="brand-accent">Quest</span>
    </div>

    <div class="nav-links">
      <!-- Admin Links -->
      <template v-if="auth.isAdmin">
        <router-link to="/admin/dashboard">Dashboard</router-link>
        <router-link to="/admin/treks">Treks</router-link>
        <router-link to="/admin/staff">Staff</router-link>
        <router-link to="/admin/users">Users</router-link>
        <router-link to="/admin/bookings">Bookings</router-link>
      </template>

      <!-- Staff Links -->
      <template v-else-if="auth.isStaff">
        <router-link to="/staff/dashboard">Dashboard</router-link>
        <router-link to="/staff/treks">My Treks</router-link>
      </template>

      <!-- User Links -->
      <template v-else-if="auth.isUser">
        <router-link to="/user/dashboard">Home</router-link>
        <router-link to="/user/treks">Explore</router-link>
        <router-link to="/user/bookings">My Bookings</router-link>
        <router-link to="/user/history">History</router-link>
        <router-link to="/user/profile">Profile</router-link>
      </template>
    </div>

    <div class="nav-user">
      <div class="avatar">{{ auth.userName?.charAt(0).toUpperCase() }}</div>
      <span class="user-name">{{ auth.userName }}</span>
      <button class="btn btn-sm btn-outline" @click="logout">Logout</button>
    </div>
  </nav>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'NavBar',
  setup() {
    const auth = useAuthStore()
    const router = useRouter()

    const logout = () => {
      auth.logout()
      router.push('/login')
    }

    return { auth, logout }
  }
}
</script>

<style scoped>
.navbar {
  background: var(--forest);
  padding: 0.75rem 2rem;
  display: flex;
  align-items: center;
  gap: 2rem;
  box-shadow: 0 2px 20px rgba(0,0,0,0.2);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-brand {
  font-size: 1.4rem;
  font-weight: 900;
  color: var(--mist);
  white-space: nowrap;
}

.nav-icon { color: var(--sage); margin-right: 0.5rem; }
.brand-accent { color: var(--sage); }

.nav-links {
  display: flex;
  gap: 0.25rem;
  flex: 1;
}

.nav-links a {
  color: rgba(183,228,199,0.8);
  text-decoration: none;
  padding: 0.5rem 0.9rem;
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 500;
  transition: all 0.2s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: white;
  background: rgba(82,183,136,0.2);
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: var(--sage);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
}

.user-name {
  color: var(--mist);
  font-size: 0.88rem;
  font-weight: 500;
}

.btn-outline {
  border-color: rgba(183,228,199,0.4) !important;
  color: var(--mist) !important;
  font-size: 0.8rem !important;
  padding: 0.3rem 0.8rem !important;
}

.btn-outline:hover {
  background: rgba(183,228,199,0.1) !important;
  color: white !important;
}
</style>
