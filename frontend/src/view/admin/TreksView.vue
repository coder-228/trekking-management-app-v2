<template>
  <div class="main">
    <div class="page-header" style="display:flex;justify-content:space-between;align-items:center;">
      <h2>Manage Treks</h2>
      <button class="btn btn-forest" @click="showModal = true; editTrek = null; resetForm()">
        + New Trek
      </button>
    </div>

    <!-- Filters -->
    <div class="card" style="margin-bottom:1rem;padding:1rem;">
      <div style="display:flex;gap:0.75rem;flex-wrap:wrap;">
        <input v-model="search" type="text" placeholder="Search treks..."
               style="flex:1;min-width:200px;padding:0.5rem 0.9rem;border:1.5px solid rgba(26,61,43,0.15);border-radius:10px;outline:none;" />
        <select v-model="filterDifficulty"
                style="padding:0.5rem;border:1.5px solid rgba(26,61,43,0.15);border-radius:10px;outline:none;">
          <option value="">All Difficulty</option>
          <option>Easy</option>
          <option>Moderate</option>
          <option>Hard</option>
        </select>
        <select v-model="filterStatus"
                style="padding:0.5rem;border:1.5px solid rgba(26,61,43,0.15);border-radius:10px;outline:none;">
          <option value="">All Status</option>
          <option>Pending</option>
          <option>Approved</option>
          <option>Open</option>
          <option>Closed</option>
          <option>Completed</option>
        </select>
        <button class="btn btn-forest" @click="fetchTreks">Filter</button>
        <button class="btn btn-outline" @click="clearFilters">Clear</button>
      </div>
    </div>

    <!-- Table -->
    <div class="card" style="padding:0;overflow:hidden;">
      <div v-if="loading" class="empty-state"><p>Loading...</p></div>
      <div v-else-if="treks.length === 0" class="empty-state">
        <h4>No treks found</h4>
      </div>
      <div v-else style="overflow-x:auto;">
        <table>
          <thead>
            <tr>
              <th>Trek</th>
              <th>Difficulty</th>
              <th>Slots</th>
              <th>Staff</th>
              <th>Status</th>
              <th>Price</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="trek in treks" :key="trek.id">
              <td>
                <div style="font-weight:600;">{{ trek.name }}</div>
                <div style="font-size:0.78rem;color:#6c757d;">{{ trek.location }}</div>
              </td>
              <td><span :class="`badge badge-${trek.difficulty.toLowerCase()}`">{{ trek.difficulty }}</span></td>
              <td>{{ trek.available_slots }}/{{ trek.total_slots }}</td>
              <td style="font-size:0.85rem;">{{ trek.staff_name || 'Unassigned' }}</td>
              <td><span :class="`badge badge-${trek.status.toLowerCase()}`">{{ trek.status }}</span></td>
              <td>{{ trek.price > 0 ? '₹' + trek.price : 'Free' }}</td>
              <td>
                <div style="display:flex;gap:0.5rem;">
                  <button class="btn btn-sm btn-outline" @click="openEdit(trek)">Edit</button>
                  <button class="btn btn-sm btn-ember" @click="deleteTrek(trek.id)">Del</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-box card">
        <h5 style="font-weight:700;color:var(--forest);margin-bottom:1.5rem;">
          {{ editTrek ? 'Edit Trek' : 'New Trek' }}
        </h5>
        <form @submit.prevent="saveTrek">
          <div class="grid-2">
            <div class="form-group">
              <label>Name *</label>
              <input v-model="form.name" required />
            </div>
            <div class="form-group">
              <label>Location *</label>
              <input v-model="form.location" required />
            </div>
            <div class="form-group">
              <label>Difficulty *</label>
              <select v-model="form.difficulty" required>
                <option>Easy</option>
                <option>Moderate</option>
                <option>Hard</option>
              </select>
            </div>
            <div class="form-group">
              <label>Status</label>
              <select v-model="form.status">
                <option>Pending</option>
                <option>Approved</option>
                <option>Open</option>
                <option>Closed</option>
                <option>Completed</option>
              </select>
            </div>
            <div class="form-group">
              <label>Duration (days) *</label>
              <input v-model="form.duration_days" type="number" min="1" required />
            </div>
            <div class="form-group">
              <label>Total Slots *</label>
              <input v-model="form.total_slots" type="number" min="1" required />
            </div>
            <div class="form-group">
              <label>Price (₹)</label>
              <input v-model="form.price" type="number" min="0" />
            </div>
            <div class="form-group">
              <label>Altitude</label>
              <input v-model="form.altitude" placeholder="e.g. 3583m" />
            </div>
            <div class="form-group">
              <label>Start Date</label>
              <input v-model="form.start_date" type="date" />
            </div>
            <div class="form-group">
              <label>End Date</label>
              <input v-model="form.end_date" type="date" />
            </div>
            <div class="form-group">
              <label>Assign Staff</label>
              <select v-model="form.staff_id">
                <option value="">-- None --</option>
                <option v-for="s in staffList" :key="s.id" :value="s.id">
                  {{ s.name }}
                </option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="form.description" rows="3"></textarea>
          </div>
          <div v-if="formError" class="alert alert-danger">{{ formError }}</div>
          <div style="display:flex;gap:0.75rem;margin-top:1rem;">
            <button type="submit" class="btn btn-forest">
              {{ editTrek ? 'Update' : 'Create' }}
            </button>
            <button type="button" class="btn btn-outline" @click="showModal = false">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'AdminTreks',
  setup() {
    const treks = ref([])
    const staffList = ref([])
    const loading = ref(false)
    const showModal = ref(false)
    const editTrek = ref(null)
    const formError = ref(null)
    const search = ref('')
    const filterDifficulty = ref('')
    const filterStatus = ref('')

    const form = ref({
      name: '', location: '', description: '',
      difficulty: 'Easy', status: 'Pending',
      duration_days: '', total_slots: '',
      price: 0, altitude: '',
      start_date: '', end_date: '', staff_id: ''
    })

    const resetForm = () => {
      form.value = {
        name: '', location: '', description: '',
        difficulty: 'Easy', status: 'Pending',
        duration_days: '', total_slots: '',
        price: 0, altitude: '',
        start_date: '', end_date: '', staff_id: ''
      }
      formError.value = null
    }

    const fetchTreks = async () => {
      loading.value = true
      try {
        const params = {}
        if (search.value) params.search = search.value
        if (filterDifficulty.value) params.difficulty = filterDifficulty.value
        if (filterStatus.value) params.status = filterStatus.value
        const res = await axios.get('/api/admin/treks', { params })
        treks.value = res.data
      } catch (e) {
        console.error(e)
      }
      loading.value = false
    }

    const fetchStaff = async () => {
      try {
        const res = await axios.get('/api/admin/staff')
        staffList.value = res.data.filter(s => s.status === 'active')
      } catch (e) { console.error(e) }
    }

    const clearFilters = () => {
      search.value = ''
      filterDifficulty.value = ''
      filterStatus.value = ''
      fetchTreks()
    }

    const openEdit = (trek) => {
      editTrek.value = trek
      form.value = {
        name: trek.name,
        location: trek.location,
        description: trek.description || '',
        difficulty: trek.difficulty,
        status: trek.status,
        duration_days: trek.duration_days,
        total_slots: trek.total_slots,
        price: trek.price,
        altitude: trek.altitude || '',
        start_date: trek.start_date || '',
        end_date: trek.end_date || '',
        staff_id: trek.staff_id || ''
      }
      showModal.value = true
    }

    const saveTrek = async () => {
      formError.value = null
      try {
        const payload = { ...form.value }
        if (!payload.staff_id) payload.staff_id = null

        if (editTrek.value) {
          await axios.put(`/api/admin/treks/${editTrek.value.id}`, payload)
        } else {
          await axios.post('/api/admin/treks', payload)
        }
        showModal.value = false
        resetForm()
        fetchTreks()
      } catch (e) {
        formError.value = e.response?.data?.error ||
          e.response?.data?.errors?.join(', ') || 'Error saving trek'
      }
    }

    const deleteTrek = async (id) => {
      if (!confirm('Delete this trek?')) return
      try {
        await axios.delete(`/api/admin/treks/${id}`)
        fetchTreks()
      } catch (e) { console.error(e) }
    }

    onMounted(() => {
      fetchTreks()
      fetchStaff()
    })

    return {
      treks, staffList, loading, showModal,
      editTrek, form, formError,
      search, filterDifficulty, filterStatus,
      fetchTreks, clearFilters,
      openEdit, saveTrek, deleteTrek, resetForm
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}
.modal-box {
  width: 100%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
}
</style>