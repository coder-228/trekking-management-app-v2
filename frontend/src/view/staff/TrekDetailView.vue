<template>
  <div class="main">
    <div class="page-header" style="display:flex;justify-content:space-between;">
      <div>
        <h2>{{ trek?.name }}</h2>
        <router-link to="/staff/treks" style="color:var(--moss);font-size:0.88rem;">
          ← Back to Treks
        </router-link>
      </div>
      <span v-if="trek" :class="`badge badge-${trek.status.toLowerCase()}`"
            style="font-size:0.9rem;padding:0.5rem 1rem;">
        {{ trek.status }}
      </span>
    </div>

    <div v-if="loading" class="empty-state"><p>Loading...</p></div>
    <div v-else-if="trek" class="grid-2">
      <!-- Trek Info + Update Form -->
      <div>
        <div class="card" style="margin-bottom:1rem;">
          <div style="background:linear-gradient(135deg,var(--forest),var(--moss));
                      margin:-1.5rem -1.5rem 1rem;padding:1.5rem;color:white;
                      border-radius:var(--card-radius) var(--card-radius) 0 0;">
            <span :class="`badge badge-${trek.difficulty.toLowerCase()}`">
              {{ trek.difficulty }}
            </span>
            <p style="margin-top:0.5rem;opacity:0.8;font-size:0.85rem;">
              📍 {{ trek.location }}
              {{ trek.altitude ? '· ' + trek.altitude : '' }}
            </p>
            <div class="slots-bar" style="margin-top:0.75rem;">
              <div class="slots-fill" :style="`width:${trek.completion_percent}%`"></div>
            </div>
            <p style="font-size:0.75rem;opacity:0.7;margin-top:4px;">
              {{ trek.booked_slots }}/{{ trek.total_slots }} booked
            </p>
          </div>

          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;
                      padding-bottom:1rem;border-bottom:1px solid rgba(26,61,43,0.08);">
            <div>
              <div style="font-size:0.75rem;color:#6c757d;">Duration</div>
              <div style="font-weight:700;">{{ trek.duration_days }} days</div>
            </div>
            <div>
              <div style="font-size:0.75rem;color:#6c757d;">Available Slots</div>
              <div style="font-weight:700;color:var(--moss);">{{ trek.available_slots }}</div>
            </div>
            <div>
              <div style="font-size:0.75rem;color:#6c757d;">Start Date</div>
              <div style="font-weight:700;">{{ trek.start_date || '—' }}</div>
            </div>
            <div>
              <div style="font-size:0.75rem;color:#6c757d;">Price</div>
              <div style="font-weight:700;color:var(--ember);">
                {{ trek.price > 0 ? '₹' + trek.price : 'Free' }}
              </div>
            </div>
          </div>

          <p v-if="trek.description" style="margin-top:1rem;font-size:0.88rem;color:#6c757d;">
            {{ trek.description }}
          </p>
        </div>

        <!-- Update Form -->
        <div class="card">
          <h6 style="font-weight:700;color:var(--forest);margin-bottom:1rem;">
            Update Trek
          </h6>
          <form @submit.prevent="updateTrek">
            <div class="form-group">
              <label>Trek Status</label>
              <select v-model="updateForm.status">
                <option>Open</option>
                <option>Closed</option>
                <option>Completed</option>
              </select>
            </div>
            <div class="form-group">
              <label>Available Slots</label>
              <input v-model="updateForm.available_slots"
                     type="number" :min="trek.booked_slots" />
              <small style="color:#6c757d;font-size:0.78rem;">
                Min: {{ trek.booked_slots }} (currently booked)
              </small>
            </div>
            <div v-if="updateError" class="alert alert-danger">{{ updateError }}</div>
            <div v-if="updateSuccess" class="alert alert-success">{{ updateSuccess }}</div>
            <button type="submit" class="btn btn-forest" style="width:100%;">
              Update Trek
            </button>
          </form>
        </div>
      </div>

      <!-- Participants -->
      <div class="card" style="padding:0;overflow:hidden;align-self:start;">
        <div style="padding:1rem 1.5rem;border-bottom:1px solid rgba(26,61,43,0.08);
                    display:flex;justify-content:space-between;align-items:center;">
          <h6 style="font-weight:700;color:var(--forest);">
            Participants
            <span style="background:var(--ember);color:white;border-radius:20px;
                         padding:2px 8px;font-size:0.72rem;margin-left:0.5rem;">
              {{ bookings.length }}
            </span>
          </h6>
        </div>
        <div v-if="bookings.length === 0" class="empty-state" style="padding:2rem;">
          <h4>No Participants Yet</h4>
        </div>
        <div v-else style="overflow-x:auto;">
          <table>
            <thead>
              <tr>
                <th>Trekker</th>
                <th>Contact</th>
                <th>Group</th>
                <th>Booked</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="b in bookings" :key="b.id">
                <td>
                  <div style="font-weight:600;font-size:0.88rem;">{{ b.user_name }}</div>
                </td>
                <td style="font-size:0.82rem;color:#6c757d;">—</td>
                <td style="text-align:center;">{{ b.num_participants }}</td>
                <td style="font-size:0.8rem;color:#6c757d;">{{ b.booking_date }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

export default {
  name: 'StaffTrekDetail',
  setup() {
    const route = useRoute()
    const trek = ref(null)
    const bookings = ref([])
    const loading = ref(false)
    const updateError = ref(null)
    const updateSuccess = ref(null)

    const updateForm = ref({
      status: '',
      available_slots: 0
    })

    const fetchData = async () => {
      loading.value = true
      try {
        const res = await axios.get(`/api/staff/treks/${route.params.id}`)
        trek.value = res.data.trek
        bookings.value = res.data.bookings
        updateForm.value.status = trek.value.status
        updateForm.value.available_slots = trek.value.available_slots
      } catch (e) { console.error(e) }
      loading.value = false
    }

    const updateTrek = async () => {
      updateError.value = null
      updateSuccess.value = null
      try {
        await axios.put(`/api/staff/treks/${route.params.id}`, updateForm.value)
        updateSuccess.value = 'Trek updated successfully!'
        fetchData()
      } catch (e) {
        updateError.value = e.response?.data?.error || 'Update failed'
      }
    }

    onMounted(fetchData)
    return { trek, bookings, loading, updateForm, updateError, updateSuccess, updateTrek }
  }
}
</script>

<style scoped>
.slots-bar {
  height: 6px;
  background: rgba(255,255,255,0.2);
  border-radius: 3px;
  overflow: hidden;
}
.slots-fill {
  height: 100%;
  background: var(--sage);
  border-radius: 3px;
}
</style>