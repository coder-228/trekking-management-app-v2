<template>
  <div class="main" style="max-width:960px;">
    <router-link to="/user/treks"
                 style="color:var(--moss);font-size:0.88rem;display:block;margin-bottom:1rem;">
      ← Back to Treks
    </router-link>

    <div v-if="loading" class="empty-state"><p>Loading...</p></div>
    <div v-else-if="trek" class="grid-2" style="align-items:start;">
      <!-- Trek Info -->
      <div class="card">
        <div style="background:linear-gradient(135deg,var(--forest),var(--moss));
                    margin:-1.5rem -1.5rem 1.5rem;padding:2rem;color:white;
                    border-radius:var(--card-radius) var(--card-radius) 0 0;">
          <span :class="`badge badge-${trek.difficulty.toLowerCase()}`">
            {{ trek.difficulty }}
          </span>
          <h3 style="font-size:1.5rem;font-weight:700;margin:0.5rem 0 0.25rem;">
            {{ trek.name }}
          </h3>
          <p style="opacity:0.8;font-size:0.88rem;">📍 {{ trek.location }}</p>
          <p v-if="trek.altitude" style="opacity:0.7;font-size:0.82rem;">
            ↑ {{ trek.altitude }}
          </p>
        </div>

        <div style="display:grid;grid-template-columns:repeat(4,1fr);
                    gap:1rem;text-align:center;padding-bottom:1rem;
                    border-bottom:1px solid rgba(26,61,43,0.08);">
          <div>
            <div style="font-size:0.72rem;color:#6c757d;">Duration</div>
            <div style="font-weight:700;color:var(--forest);">{{ trek.duration_days }}d</div>
          </div>
          <div>
            <div style="font-size:0.72rem;color:#6c757d;">Available</div>
            <div style="font-weight:700;color:var(--moss);">{{ trek.available_slots }}</div>
          </div>
          <div>
            <div style="font-size:0.72rem;color:#6c757d;">Start</div>
            <div style="font-weight:700;color:var(--forest);">
              {{ trek.start_date || 'TBD' }}
            </div>
          </div>
          <div>
            <div style="font-size:0.72rem;color:#6c757d;">Price</div>
            <div style="font-weight:700;color:var(--ember);">
              {{ trek.price > 0 ? '₹' + trek.price : 'Free' }}
            </div>
          </div>
        </div>

        <p v-if="trek.description"
           style="margin-top:1rem;color:#6c757d;font-size:0.9rem;line-height:1.7;">
          {{ trek.description }}
        </p>

        <div v-if="trek.staff_name"
             style="margin-top:1rem;background:rgba(82,183,136,0.08);
                    border-radius:10px;padding:1rem;">
          <div style="font-size:0.78rem;color:#6c757d;">Trek Guide</div>
          <div style="font-weight:600;color:var(--forest);">{{ trek.staff_name }}</div>
        </div>
      </div>

      <!-- Booking Card -->
      <div class="card" style="position:sticky;top:80px;">
        <h6 style="font-weight:700;color:var(--forest);margin-bottom:1rem;">
          Book This Trek
        </h6>

        <div v-if="alreadyBooked"
             style="text-align:center;background:rgba(82,183,136,0.1);
                    border-radius:10px;padding:1.5rem;">
          <div style="font-size:2rem;">✅</div>
          <div style="font-weight:700;color:var(--forest);margin-top:0.5rem;">
            Already Booked!
          </div>
          <router-link to="/user/bookings"
                       class="btn btn-outline btn-sm"
                       style="margin-top:0.75rem;display:inline-block;">
            View Bookings
          </router-link>
        </div>

        <div v-else-if="trek.status === 'Approved'" class="alert alert-warning">
          ⏰ This trek is approved but not yet open for booking. Check back soon!
        </div>

        <div v-else-if="trek.status !== 'Open'" class="alert alert-danger">
          This trek is currently <strong>{{ trek.status }}</strong>.
        </div>

        <div v-else-if="trek.available_slots === 0" class="alert alert-danger">
          ❌ Fully booked! No slots available.
        </div>

        <form v-else @submit.prevent="bookTrek">
          <div class="form-group">
            <label>Number of Participants</label>
            <input v-model="bookForm.num_participants"
                   type="number" min="1" :max="trek.available_slots" />
            <small style="color:#6c757d;font-size:0.78rem;">
              Max: {{ trek.available_slots }}
            </small>
          </div>
          <div class="form-group">
            <label>Special Requirements</label>
            <textarea v-model="bookForm.special_requirements" rows="3"
                      placeholder="Dietary requirements, medical conditions..."></textarea>
          </div>
          <div v-if="trek.price > 0"
               style="background:rgba(231,111,81,0.08);border-radius:10px;
                      padding:0.75rem;margin-bottom:1rem;">
            <div style="font-size:0.78rem;color:#6c757d;">Price per person</div>
            <div style="font-weight:700;color:var(--ember);font-size:1.1rem;">
              ₹{{ trek.price }}
            </div>
          </div>
          <div v-if="bookError" class="alert alert-danger">{{ bookError }}</div>
          <div v-if="bookSuccess" class="alert alert-success">{{ bookSuccess }}</div>
          <button type="submit" class="btn btn-forest"
                  style="width:100%;" :disabled="booking">
            {{ booking ? 'Booking...' : 'Confirm Booking' }}
          </button>
        </form>

        <div style="margin-top:1rem;padding-top:1rem;
                    border-top:1px solid rgba(26,61,43,0.08);">
          <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
            <span style="color:var(--sage);">✓</span>
            <span style="font-size:0.82rem;color:#6c757d;">Secure booking</span>
          </div>
          <div style="display:flex;align-items:center;gap:0.5rem;">
            <span style="color:var(--sage);">✓</span>
            <span style="font-size:0.82rem;color:#6c757d;">Free cancellation</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'UserTrekDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const trek = ref(null)
    const loading = ref(false)
    const alreadyBooked = ref(false)
    const booking = ref(false)
    const bookError = ref(null)
    const bookSuccess = ref(null)

    const bookForm = ref({
      num_participants: 1,
      special_requirements: ''
    })

    const fetchTrek = async () => {
      loading.value = true
      try {
        const res = await axios.get(`/api/user/treks/${route.params.id}`)
        trek.value = res.data

        const bookings = await axios.get('/api/user/bookings', {
          params: { status: 'Booked' }
        })
        alreadyBooked.value = bookings.data.some(
          b => b.trek_id === trek.value.id
        )
      } catch (e) { console.error(e) }
      loading.value = false
    }

    const bookTrek = async () => {
      if (!confirm(`Confirm booking for ${trek.value.name}?`)) return
      booking.value = true
      bookError.value = null
      bookSuccess.value = null
      try {
        await axios.post('/api/user/bookings', {
          trek_id: trek.value.id,
          num_participants: parseInt(bookForm.value.num_participants),
          special_requirements: bookForm.value.special_requirements
        })
        bookSuccess.value = `Successfully booked ${trek.value.name}! 🎉`
        setTimeout(() => router.push('/user/bookings'), 1500)
      } catch (e) {
        bookError.value = e.response?.data?.error || 'Booking failed'
      }
      booking.value = false
    }

    onMounted(fetchTrek)
    return {
      trek, loading, alreadyBooked,
      bookForm, booking, bookError, bookSuccess, bookTrek
    }
  }
}
</script>