<template>
  <div class="main">
    <div class="page-header">
      <h2>My Assigned Treks</h2>
    </div>

    <div v-if="loading" class="empty-state"><p>Loading...</p></div>
    <div v-else-if="treks.length === 0" class="empty-state card">
      <h4>No Treks Assigned</h4>
      <p>Contact admin to get treks assigned to you.</p>
    </div>
    <div v-else class="grid-3">
      <div v-for="trek in treks" :key="trek.id" class="trek-card card">
        <div class="trek-header">
          <span :class="`badge badge-${trek.difficulty.toLowerCase()}`">
            {{ trek.difficulty }}
          </span>
          <h6>{{ trek.name }}</h6>
          <p>{{ trek.location }}</p>
        </div>
        <div class="trek-body">
          <div class="trek-stats">
            <div>
              <div class="stat-label">Duration</div>
              <div class="stat-val">{{ trek.duration_days }}d</div>
            </div>
            <div>
              <div class="stat-label">Booked</div>
              <div class="stat-val">{{ trek.booked_slots }}/{{ trek.total_slots }}</div>
            </div>
            <div>
              <div class="stat-label">Status</div>
              <span :class="`badge badge-${trek.status.toLowerCase()}`">
                {{ trek.status }}
              </span>
            </div>
          </div>
          <div class="slots-bar">
            <div class="slots-fill"
                 :style="`width:${trek.completion_percent}%`">
            </div>
          </div>
          <router-link :to="`/staff/treks/${trek.id}`"
                       class="btn btn-forest"
                       style="width:100%;text-align:center;margin-top:0.75rem;display:block;">
            Manage Trek
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'StaffTreks',
  setup() {
    const treks = ref([])
    const loading = ref(false)

    onMounted(async () => {
      loading.value = true
      try {
        const res = await axios.get('/api/staff/treks')
        treks.value = res.data
      } catch (e) { console.error(e) }
      loading.value = false
    })

    return { treks, loading }
  }
}
</script>

<style scoped>
.trek-card { padding: 0; overflow: hidden; }
.trek-header {
  background: linear-gradient(135deg, var(--forest), var(--moss));
  padding: 1.25rem;
  color: white;
}
.trek-header h6 {
  font-weight: 700;
  margin: 0.5rem 0 0.25rem;
  font-size: 1rem;
}
.trek-header p { font-size: 0.82rem; opacity: 0.8; margin: 0; }
.trek-body { padding: 1rem; }
.trek-stats {
  display: flex;
  justify-content: space-around;
  text-align: center;
  margin-bottom: 0.75rem;
}
.stat-label { font-size: 0.7rem; color: #6c757d; }
.stat-val { font-weight: 700; color: var(--forest); font-size: 0.9rem; }
.slots-bar {
  height: 6px;
  background: rgba(26,61,43,0.1);
  border-radius: 3px;
  overflow: hidden;
}
.slots-fill {
  height: 100%;
  background: var(--sage);
  border-radius: 3px;
  transition: width 0.5s;
}
</style>