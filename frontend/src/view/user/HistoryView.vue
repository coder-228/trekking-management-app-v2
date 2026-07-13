<template>
  <div class="main">
    <div class="page-header">
      <h2>Trekking History</h2>
      <p style="color:#6c757d;">Your completed and cancelled adventures</p>
    </div>

    <!-- Completed -->
    <div v-if="completed.length" style="margin-bottom:2rem;">
      <h5 style="color:var(--forest);margin-bottom:1rem;">
        🏆 Completed Treks ({{ completed.length }})
      </h5>
      <div class="grid-3">
        <div v-for="b in completed" :key="b.id"
             class="card" style="border-left:4px solid var(--sage);">
          <div style="display:flex;justify-content:space-between;align-items:start;">
            <div>
              <h6 style="font-weight:700;color:var(--forest);">{{ b.trek_name }}</h6>
              <p style="font-size:0.8rem;color:#6c757d;">📍 {{ b.trek_location }}</p>
            </div>
            <span style="font-size:1.5rem;">✅</span>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;
                      text-align:center;margin:0.75rem 0;
                      padding:0.75rem 0;border-top:1px solid rgba(26,61,43,0.06);
                      border-bottom:1px solid rgba(26,61,43,0.06);">
            <div>
              <div style="font-size:0.68rem;color:#6c757d;">Difficulty</div>
              <span :class="`badge badge-${b.trek_difficulty?.toLowerCase()}`"
                    style="font-size:0.68rem;">{{ b.trek_difficulty }}</span>
            </div>
            <div>
              <div style="font-size:0.68rem;color:#6c757d;">Group</div>
              <div style="font-weight:700;color:var(--forest);">{{ b.num_participants }}</div>
            </div>
            <div>
              <div style="font-size:0.68rem;color:#6c757d;">Date</div>
              <div style="font-weight:700;font-size:0.8rem;color:var(--forest);">
                {{ b.booking_date }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Cancelled -->
    <div v-if="cancelled.length">
      <h5 style="color:var(--forest);margin-bottom:1rem;">
        ❌ Cancelled Bookings ({{ cancelled.length }})
      </h5>
      <div class="grid-3">
        <div v-for="b in cancelled" :key="b.id"
             class="card" style="border-left:4px solid var(--ember);opacity:0.85;">
          <div style="display:flex;justify-content:space-between;align-items:start;">
            <div>
              <h6 style="font-weight:700;color:var(--forest);">{{ b.trek_name }}</h6>
              <p style="font-size:0.8rem;color:#6c757d;">📍 {{ b.trek_location }}</p>
            </div>
            <span style="font-size:1.5rem;opacity:0.5;">❌</span>
          </div>
          <div style="font-size:0.82rem;color:#6c757d;margin-top:0.5rem;">
            Booked on: {{ b.booking_date }}
          </div>
        </div>
      </div>
    </div>

    <div v-if="!completed.length && !cancelled.length" class="card empty-state">
      <h4>No History Yet</h4>
      <p>Your completed and cancelled treks will appear here.</p>
      <router-link to="/user/treks" class="btn btn-forest btn-sm"
                   style="margin-top:0.75rem;display:inline-block;">
        Explore Treks
      </router-link>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'UserHistory',
  setup() {
    const completed = ref([])
    const cancelled = ref([])

    onMounted(async () => {
      try {
        const res = await axios.get('/api/user/history')
        completed.value = res.data.completed
        cancelled.value = res.data.cancelled
      } catch (e) { console.error(e) }
    })

    return { completed, cancelled }
  }
}
</script>