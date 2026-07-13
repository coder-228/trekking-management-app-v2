<template>
  <div class="main">
    <div class="page-header">
      <h2>Explore Treks</h2>
      <p style="color:#6c757d;">Find your next adventure</p>
    </div>

    <!-- Filters -->
    <div class="card" style="margin-bottom:1.5rem;padding:1rem;">
      <div style="display:flex;gap:0.75rem;flex-wrap:wrap;">
        <input v-model="search" type="text" placeholder="Search treks..."
               style="flex:1;min-width:180px;padding:0.5rem 0.9rem;
                      border:1.5px solid rgba(26,61,43,0.15);border-radius:10px;outline:none;" />
        <select v-model="difficulty"
                style="padding:0.5rem;border:1.5px solid rgba(26,61,43,0.15);
                       border-radius:10px;outline:none;">
          <option value="">All Levels</option>
          <option>Easy</option>
          <option>Moderate</option>
          <option>Hard</option>
        </select>
        <input v-model="location" type="text" placeholder="Location..."
               style="width:150px;padding:0.5rem 0.9rem;
                      border:1.5px solid rgba(26,61,43,0.15);border-radius:10px;outline:none;" />
        <input v-model="maxPrice" type="number" placeholder="Max price ₹"
               style="width:130px;padding:0.5rem 0.9rem;
                      border:1.5px solid rgba(26,61,43,0.15);border-radius:10px;outline:none;" />
        <button class="btn btn-forest" @click="fetchTreks">Filter</button>
        <button class="btn btn-outline" @click="clearFilters">Clear</button>
      </div>
    </div>

    <div v-if="loading" class="empty-state"><p>Loading...</p></div>
    <div v-else-if="treks.length === 0" class="card empty-state">
      <h4>No Treks Found</h4>
      <button class="btn btn-forest btn-sm" @click="clearFilters"
              style="margin-top:0.75rem;">
        Clear Filters
      </button>
    </div>
    <div v-else>
      <p style="color:#6c757d;font-size:0.88rem;margin-bottom:1rem;">
        {{ treks.length }} trek(s) found
      </p>
      <div class="grid-3">
        <div v-for="trek in treks" :key="trek.id" class="trek-card card">
          <div class="trek-header">
            <span :class="`badge badge-${trek.difficulty.toLowerCase()}`">
              {{ trek.difficulty }}
            </span>
            <h6>{{ trek.name }}</h6>
            <p>📍 {{ trek.location }}</p>
            <p v-if="trek.altitude" style="font-size:0.78rem;opacity:0.7;">
              ↑ {{ trek.altitude }}
            </p>
            <div class="slots-bar">
              <div class="slots-fill"
                   :style="`width:${100 - (trek.available_slots/trek.total_slots*100)}%`">
              </div>
            </div>
            <p style="font-size:0.75rem;opacity:0.7;margin-top:4px;">
              {{ trek.available_slots }} of {{ trek.total_slots }} slots available
            </p>
          </div>
          <div class="trek-body">
            <div class="trek-stats">
              <div>
                <div class="stat-label">Duration</div>
                <div class="stat-val">{{ trek.duration_days }}d</div>
              </div>
              <div>
                <div class="stat-label">Price</div>
                <div class="stat-val" style="color:var(--ember);">
                  {{ trek.price > 0 ? '₹' + trek.price : 'Free' }}
                </div>
              </div>
              <div>
                <div class="stat-label">Start</div>
                <div class="stat-val">{{ trek.start_date || 'TBD' }}</div>
              </div>
            </div>

            <p v-if="trek.description" class="trek-desc">
              {{ trek.description.substring(0, 80) }}...
            </p>

            <!-- Button based on status -->
            <div v-if="trek.status === 'Approved'"
                 class="btn" style="width:100%;text-align:center;cursor:default;
                                    background:rgba(244,162,97,0.15);color:var(--gold);
                                    border:1px solid var(--gold);">
              ⏰ Opening Soon
            </div>
            <div v-else-if="trek.available_slots === 0"
                 class="btn" style="width:100%;text-align:center;cursor:default;
                                    background:#f0f0f0;color:#999;">
              Fully Booked
            </div>
            <router-link v-else :to="`/user/treks/${trek.id}`"
                         class="btn btn-forest"
                         style="width:100%;text-align:center;display:block;">
              View & Book
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'UserTreks',
  setup() {
    const treks = ref([])
    const loading = ref(false)
    const search = ref('')
    const difficulty = ref('')
    const location = ref('')
    const maxPrice = ref('')

    const fetchTreks = async () => {
      loading.value = true
      try {
        const params = {}
        if (search.value) params.search = search.value
        if (difficulty.value) params.difficulty = difficulty.value
        if (location.value) params.location = location.value
        if (maxPrice.value) params.max_price = maxPrice.value
        const res = await axios.get('/api/user/treks', { params })
        treks.value = res.data
      } catch (e) { console.error(e) }
      loading.value = false
    }

    const clearFilters = () => {
      search.value = ''
      difficulty.value = ''
      location.value = ''
      maxPrice.value = ''
      fetchTreks()
    }

    onMounted(fetchTreks)
    return { treks, loading, search, difficulty, location, maxPrice, fetchTreks, clearFilters }
  }
}
</script>

<style scoped>
.trek-card { padding: 0; overflow: hidden; transition: transform 0.2s; }
.trek-card:hover { transform: translateY(-4px); }
.trek-header {
  background: linear-gradient(135deg, var(--forest), var(--moss));
  padding: 1.25rem;
  color: white;
}
.trek-header h6 { font-weight: 700; margin: 0.5rem 0 0.25rem; font-size: 1rem; }
.trek-header p { font-size: 0.82rem; opacity: 0.8; margin: 0 0 0.25rem; }
.trek-body { padding: 1rem; }
.trek-stats {
  display: flex;
  justify-content: space-around;
  text-align: center;
  margin-bottom: 0.75rem;
}
.stat-label { font-size: 0.7rem; color: #6c757d; }
.stat-val { font-weight: 700; color: var(--forest); font-size: 0.88rem; }
.trek-desc { font-size: 0.82rem; color: #6c757d; margin-bottom: 0.75rem; }
.slots-bar {
  height: 4px;
  background: rgba(255,255,255,0.2);
  border-radius: 3px;
  overflow: hidden;
  margin-top: 0.5rem;
}
.slots-fill { height: 100%; background: var(--sage); border-radius: 3px; }
</style>