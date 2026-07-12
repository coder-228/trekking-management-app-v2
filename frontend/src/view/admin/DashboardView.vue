<template>
  <div class="main">
    <div class="page-header">
      <h2>Admin Dashboard</h2>
      <p style="color:#6c757d;">Welcome back, {{ auth.userName }}</p>
    </div>

    <!-- Stats -->
    <div class="grid-4" style="margin-bottom:1.5rem;">
      <div class="stat-card forest">
        <div class="stat-num">{{ stats.total_treks }}</div>
        <div class="stat-label">Total Treks</div>
      </div>
      <div class="stat-card sage">
        <div class="stat-num">{{ stats.total_users }}</div>
        <div class="stat-label">Trekkers</div>
      </div>
      <div class="stat-card gold">
        <div class="stat-num">{{ stats.total_staff }}</div>
        <div class="stat-label">Staff Members</div>
      </div>
      <div class="stat-card ember">
        <div class="stat-num">{{ stats.total_bookings }}</div>
        <div class="stat-label">Total Bookings</div>
      </div>
    </div>

    <div class="grid-2">
      <!-- Trek Status -->
      <div class="card">
        <h6 style="font-weight:700;margin-bottom:1rem;color:var(--forest);">Trek Status Overview</h6>
        <div v-for="(count, status) in stats.status_stats" :key="status"
             style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
          <span :class="`badge badge-${status.toLowerCase()}`">{{ status }}</span>
          <div style="display:flex;align-items:center;gap:0.75rem;">
            <div style="width:100px;height:6px;background:rgba(26,61,43,0.1);border-radius:3px;">
              <div :style="`width:${stats.total_treks > 0 ? (count/stats.total_treks*100) : 0}%;height:100%;background:var(--sage);border-radius:3px;`"></div>
            </div>
            <span style="font-weight:700;color:var(--forest);">{{ count }}</span>
          </div>
        </div>
      </div>

      <!-- Recent Bookings -->
      <div class="card">
        <h6 style="font-weight:700;margin-bottom:1rem;color:var(--forest);">Recent Bookings</h6>
        <div v-if="stats.recent_bookings?.length">
          <div v-for="b in stats.recent_bookings" :key="b.id"
               style="padding:0.5rem 0;border-bottom:1px solid rgba(26,61,43,0.06);">
            <div style="display:flex;justify-content:space-between;">
              <div>
                <div style="font-weight:600;font-size:0.88rem;">{{ b.user_name }}</div>
                <div style="font-size:0.78rem;color:#6c757d;">{{ b.trek_name }}</div>
              </div>
              <span :class="`badge badge-${b.status.toLowerCase()}`">{{ b.status }}</span>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <p>No bookings yet</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import axios from 'axios'

export default {
  name: 'AdminDashboard',
  setup() {
    const auth = useAuthStore()
    const stats = ref({
      total_treks: 0, total_users: 0,
      total_staff: 0, total_bookings: 0,
      status_stats: {}, recent_bookings: []
    })

    onMounted(async () => {
      try {
        const res = await axios.get('/api/admin/dashboard')
        stats.value = res.data
      } catch (e) {
        console.error(e)
      }
    })

    return { auth, stats }
  }
}
</script>

<style scoped>
.stat-card {
  border-radius: var(--card-radius);
  padding: 1.5rem;
  color: white;
  position: relative;
}
.stat-card.forest { background: linear-gradient(135deg, var(--forest), var(--moss)); }
.stat-card.sage { background: linear-gradient(135deg, var(--sage), #40916c); }
.stat-card.gold { background: linear-gradient(135deg, var(--gold), #e0801a); }
.stat-card.ember { background: linear-gradient(135deg, var(--ember), #c1440e); }
.stat-num { font-size: 2.5rem; font-weight: 900; line-height: 1; }
.stat-label { font-size: 0.85rem; opacity: 0.85; margin-top: 0.25rem; }
</style>
