<template>
  <div class="main">
    <div class="page-header">
      <h2>Staff Dashboard</h2>
      <p style="color:#6c757d;">Welcome back, {{ auth.userName }}</p>
    </div>

    <div class="grid-4" style="margin-bottom:1.5rem;">
      <div class="stat-card forest">
        <div class="stat-num">{{ data.total_treks }}</div>
        <div class="stat-label">Assigned Treks</div>
      </div>
      <div class="stat-card sage">
        <div class="stat-num">{{ data.open_treks_count }}</div>
        <div class="stat-label">Open Treks</div>
      </div>
      <div class="stat-card gold">
        <div class="stat-num">{{ data.total_participants }}</div>
        <div class="stat-label">Total Participants</div>
      </div>
      <div class="stat-card ember">
        <div class="stat-num">{{ auth.user?.experience_years }}</div>
        <div class="stat-label">Years Experience</div>
      </div>
    </div>

    <div class="card" style="padding:0;overflow:hidden;">
      <div style="padding:1rem 1.5rem;border-bottom:1px solid rgba(26,61,43,0.08);
                  display:flex;justify-content:space-between;align-items:center;">
        <h6 style="font-weight:700;color:var(--forest);">My Assigned Treks</h6>
        <router-link to="/staff/treks" class="btn btn-sm btn-outline">View All</router-link>
      </div>
      <div v-if="loading" class="empty-state"><p>Loading...</p></div>
      <div v-else-if="!data.assigned_treks?.length" class="empty-state">
        <h4>No Treks Assigned</h4>
        <p>Contact admin to get treks assigned.</p>
      </div>
      <div v-else style="overflow-x:auto;">
        <table>
          <thead>
            <tr>
              <th>Trek</th>
              <th>Difficulty</th>
              <th>Participants</th>
              <th>Status</th>
              <th>Start Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="trek in data.assigned_treks" :key="trek.id">
              <td>
                <div style="font-weight:600;">{{ trek.name }}</div>
                <div style="font-size:0.78rem;color:#6c757d;">{{ trek.location }}</div>
              </td>
              <td>
                <span :class="`badge badge-${trek.difficulty.toLowerCase()}`">
                  {{ trek.difficulty }}
                </span>
              </td>
              <td>{{ trek.booked_slots }}/{{ trek.total_slots }}</td>
              <td>
                <span :class="`badge badge-${trek.status.toLowerCase()}`">
                  {{ trek.status }}
                </span>
              </td>
              <td style="font-size:0.82rem;color:#6c757d;">
                {{ trek.start_date || '—' }}
              </td>
              <td>
                <router-link :to="`/staff/treks/${trek.id}`"
                             class="btn btn-sm btn-forest">
                  Manage
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import axios from 'axios'

export default {
  name: 'StaffDashboard',
  setup() {
    const auth = useAuthStore()
    const loading = ref(false)
    const data = ref({
      total_treks: 0,
      open_treks_count: 0,
      total_participants: 0,
      assigned_treks: []
    })

    onMounted(async () => {
      loading.value = true
      try {
        const res = await axios.get('/api/staff/dashboard')
        data.value = res.data
      } catch (e) { console.error(e) }
      loading.value = false
    })

    return { auth, data, loading }
  }
}
</script>

<style scoped>
.stat-card {
  border-radius: var(--card-radius);
  padding: 1.5rem;
  color: white;
}
.stat-card.forest { background: linear-gradient(135deg, var(--forest), var(--moss)); }
.stat-card.sage { background: linear-gradient(135deg, var(--sage), #40916c); }
.stat-card.gold { background: linear-gradient(135deg, var(--gold), #e0801a); }
.stat-card.ember { background: linear-gradient(135deg, var(--ember), #c1440e); }
.stat-num { font-size: 2.5rem; font-weight: 900; line-height: 1; }
.stat-label { font-size: 0.85rem; opacity: 0.85; margin-top: 0.25rem; }
</style>
