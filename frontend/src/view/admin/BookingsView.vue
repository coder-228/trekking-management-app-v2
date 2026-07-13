<template>
  <div class="main">
    <div class="page-header">
      <h2>All Bookings</h2>
    </div>
    <div class="card" style="margin-bottom:1rem;padding:1rem;">
      <div style="display:flex;gap:0.75rem;">
        <select v-model="filterStatus"
                style="padding:0.5rem;border:1.5px solid rgba(26,61,43,0.15);border-radius:10px;outline:none;">
          <option value="">All Status</option>
          <option>Booked</option>
          <option>Cancelled</option>
          <option>Completed</option>
        </select>
        <button class="btn btn-forest" @click="fetchBookings">Filter</button>
        <button class="btn btn-outline" @click="filterStatus=''; fetchBookings()">Clear</button>
      </div>
    </div>
    <div class="card" style="padding:0;overflow:hidden;">
      <div v-if="loading" class="empty-state"><p>Loading...</p></div>
      <div v-else-if="bookings.length === 0" class="empty-state">
        <h4>No bookings found</h4>
      </div>
      <div v-else style="overflow-x:auto;">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Trekker</th>
              <th>Trek</th>
              <th>Date</th>
              <th>Participants</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in bookings" :key="b.id">
              <td style="color:#6c757d;">#{{ b.id }}</td>
              <td>
                <div style="font-weight:600;">{{ b.user_name }}</div>
              </td>
              <td>
                <div style="font-weight:600;">{{ b.trek_name }}</div>
                <div style="font-size:0.78rem;color:#6c757d;">{{ b.trek_location }}</div>
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
  </div>
</template>
<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
export default {
  name: 'AdminBookings',
  setup() {
    const bookings = ref([])
    const loading = ref(false)
    const filterStatus = ref('')
    const fetchBookings = async () => {
      loading.value = true
      try {
        const res = await axios.get('/api/admin/bookings', {
          params: filterStatus.value ? { status: filterStatus.value } : {}
        })
        bookings.value = res.data
      } catch (e) { console.error(e) }
      loading.value = false
    }
    onMounted(fetchBookings)
    return { bookings, loading, filterStatus, fetchBookings }
  }
}
</script>