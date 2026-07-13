<template>
  <div class="main">
    <div class="page-header">
      <h2>My Bookings</h2>
    </div>

    <div class="card" style="margin-bottom:1rem;padding:1rem;">
      <div style="display:flex;gap:0.75rem;">
        <select v-model="filterStatus"
                style="padding:0.5rem;border:1.5px solid rgba(26,61,43,0.15);
                       border-radius:10px;outline:none;">
          <option value="">All Bookings</option>
          <option>Booked</option>
          <option>Cancelled</option>
          <option>Completed</option>
        </select>
        <button class="btn btn-forest" @click="fetchBookings">Filter</button>
        <button class="btn btn-outline" @click="filterStatus=''; fetchBookings()">Clear</button>
      </div>
    </div>

    <div v-if="loading" class="empty-state"><p>Loading...</p></div>
    <div v-else-if="bookings.length === 0" class="card empty-state">
      <h4>No Bookings Found</h4>
      <router-link to="/user/treks" class="btn btn-forest btn-sm"
                   style="margin-top:0.75rem;display:inline-block;">
        Explore Treks
      </router-link>
    </div>
    <div v-else class="grid-3">
      <div v-for="b in bookings" :key="b.id" class="card booking-card">
        <div class="booking-header">
          <div style="display:flex;justify-content:space-between;align-items:start;">
            <div>
              <h6>{{ b.trek_name }}</h6>
              <p>📍 {{ b.trek_location }}</p>
            </div>
            <span :class="`badge badge-${b.status.toLowerCase()}`">{{ b.status }}</span>
          </div>
        </div>
        <div class="booking-body">
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;
                      text-align:center;margin-bottom:0.75rem;">
            <div>
              <div class="info-label">Difficulty</div>
              <span :class="`badge badge-${b.trek_difficulty?.toLowerCase()}`"
                    style="font-size:0.68rem;">
                {{ b.trek_difficulty }}
              </span>
            </div>
            <div>
              <div class="info-label">Persons</div>
              <div class="info-val">{{ b.num_participants }}</div>
            </div>
            <div>
              <div class="info-label">Booked</div>
              <div class="info-val">{{ b.booking_date }}</div>
            </div>
          </div>
          <div v-if="b.start_date"
               style="font-size:0.82rem;color:#6c757d;margin-bottom:0.75rem;">
            🚀 Trek Start: {{ b.start_date }}
          </div>
          <button v-if="b.status === 'Booked'"
                  class="btn btn-outline btn-sm"
                  style="width:100%;border-color:var(--ember);color:var(--ember);"
                  @click="cancelBooking(b.id)">
            Cancel Booking
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'UserBookings',
  setup() {
    const bookings = ref([])
    const loading = ref(false)
    const filterStatus = ref('')

    const fetchBookings = async () => {
      loading.value = true
      try {
        const params = filterStatus.value ? { status: filterStatus.value } : {}
        const res = await axios.get('/api/user/bookings', { params })
        bookings.value = res.data
      } catch (e) { console.error(e) }
      loading.value = false
    }

    const cancelBooking = async (id) => {
      if (!confirm('Cancel this booking?')) return
      try {
        await axios.put(`/api/user/bookings/${id}/cancel`)
        fetchBookings()
      } catch (e) { console.error(e) }
    }

    onMounted(fetchBookings)
    return { bookings, loading, filterStatus, fetchBookings, cancelBooking }
  }
}
</script>

<style scoped>
.booking-card { padding: 0; overflow: hidden; }
.booking-header {
  background: linear-gradient(135deg, var(--forest), var(--moss));
  padding: 1.25rem;
  color: white;
}
.booking-header h6 { font-weight: 700; margin-bottom: 0.25rem; }
.booking-header p { font-size: 0.82rem; opacity: 0.8; margin: 0; }
.booking-body { padding: 1rem; }
.info-label { font-size: 0.68rem; color: #6c757d; margin-bottom: 2px; }
.info-val { font-weight: 700; font-size: 0.85rem; color: var(--forest); }
</style>