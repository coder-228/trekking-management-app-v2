<template>
  <div class="main">
    <!-- Hero -->
    <div class="hero-banner">
      <div>
        <h2>Welcome back, {{ auth.userName?.split(' ')[0] }}! 🏔️</h2>
        <p>Ready for your next summit adventure?</p>
        <router-link to="/user/treks" class="btn btn-sage" style="margin-top:1rem;">
          Explore Open Treks
        </router-link>
      </div>
    </div>
    <div class="grid-4" style="margin-bottom:1.5rem;">
      <div class="stat-card forest">
        <div class="stat-num">{{ data.total_bookings }}</div>
        <div class="stat-label">Total Bookings</div>
      </div>
      <div class="stat-card sage">
        <div class="stat-num">{{ data.active_bookings?.length }}</div>
        <div class="stat-label">Active Treks</div>
      </div>
      <div class="stat-card gold">
        <div class="stat-num">{{ data.completed_count }}</div>
        <div class="stat-label">Completed</div>
      </div>
      <div class="stat-card ember">
        <div class="stat-num">{{ data.open_treks?.length }}</div>
        <div class="stat-label">Open Treks</div>
      </div>
    </div>

    <div class="grid-2">
      <!-- My Active Bookings -->
      <div class="card" style="padding:0;overflow:hidden;">
        <div style="padding:1rem 1.5rem;border-bottom:1px solid rgba(26,61,43,0.08); display:flex;justify-content:space-between;align-items:center;">
          <h6 style="font-weight:700;color:var(--forest);">My Active Bookings</h6>
          <router-link to="/user/bookings" class="btn btn-sm btn-outline">
            View All
          </router-link>
        </div>
        <div v-if="!data.active_bookings?.length" class="empty-state" style="padding:2rem;">
          <h4>No Active Bookings</h4>
          <router-link to="/user/treks" class="btn btn-forest btn-sm" style="margin-top:0.75rem;display:inline-block;">
            Browse Treks </router-link>
        </div>
        <div v-else style="overflow-x:auto;">
          <table>
            <thead>
              <tr>
                <th>Trek</th>
                <th>Date</th>
                <th>Persons</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="b in data.active_bookings" :key="b.id">
                <td>
                  <div style="font-weight:600;font-size:0.88rem;">{{ b.trek_name }}</div>
                  <div style="font-size:0.75rem;color:#6c757d;">{{ b.trek_location }}</div>
                </td>
                <td style="font-size:0.82rem;color:#6c757d;">{{ b.booking_date }}</td>
                <td style="text-align:center;">{{ b.num_participants }}</td>
                <td>
                  <span :class="`badge badge-${b.status.toLowerCase()}`">
                    {{ b.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="card" style="padding:0;overflow:hidden;">
        <div style="padding:1rem 1.5rem;border-bottom:1px solid rgba(26,61,43,0.08);
                    display:flex;justify-content:space-between;align-items:center;">
          <h6 style="font-weight:700;color:var(--forest);">Upcoming Treks</h6>
          <router-link to="/user/treks" class="btn btn-sm btn-outline">Explore</router-link>
        </div>
        <div v-if="!data.open_treks?.length" class="empty-state" style="padding:2rem;">
          <h4>No Open Treks</h4>
        </div>
        <div v-else>
          <div v-for="trek in data.open_treks" :key="trek.id"
               style="padding:0.85rem 1.25rem;border-bottom:1px solid rgba(26,61,43,0.05);">
            <div style="display:flex;justify-content:space-between;align-items:start;">
              <div>
                <div style="font-weight:600;font-size:0.88rem;">{{ trek.name }}</div>
                <div style="font-size:0.78rem;color:#6c757d;"> 📍 {{ trek.location }} · {{ trek.duration_days }}d </div>
              </div>
              <div style="text-align:right;">
                <span :class="`badge badge-${trek.difficulty.toLowerCase()}`">
                  {{ trek.difficulty }}
                </span>
                <div v-if="trek.price > 0"
                     style="font-size:0.78rem;color:var(--ember);font-weight:600;margin-top:4px;">
                  ₹{{ trek.price }}
                </div>
              </div>
            </div>
            <div style="display:flex;justify-content:space-between; align-items:center;margin-top:0.5rem;">
              <div style="font-size:0.75rem;color:#6c757d;"> {{ trek.available_slots }} slots left </div>
              <router-link :to="`/user/treks/${trek.id}`" class="btn btn-sm btn-forest"> Book </router-link>
            </div>
          </div>
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
  name: 'UserDashboard',
  setup() {
    const auth = useAuthStore()
    const data = ref({
      total_bookings: 0,
      active_bookings: [],
      completed_count: 0,
      open_treks: []
    })
    onMounted(async () => {
      try {
        const res = await axios.get('/api/user/dashboard')
        data.value = res.data
      } catch (e) { console.error(e) }
    })
    return { auth, data }
  }
}
</script>
<style scoped>
.hero-banner {
  background: linear-gradient(135deg, var(--forest), var(--moss));
  border-radius: var(--card-radius);
  padding: 2rem;
  margin-bottom: 1.5rem;
  color: white;
  position: relative;
  overflow: hidden;
}
.hero-banner h2 { font-size: 1.5rem; font-weight: 700; margin-bottom: 0.25rem; }
.hero-banner p { opacity: 0.8; }
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
