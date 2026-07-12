<template>
  <div class="main">
    <div class="page-header" style="display:flex;justify-content:space-between;align-items:center;">
      <h2>Manage Staff</h2>
      <button class="btn btn-forest" @click="showModal = true; editStaff = null; resetForm()">
        + Add Staff
      </button>
    </div>

    <!-- Search -->
    <div class="card" style="margin-bottom:1rem;padding:1rem;">
      <div style="display:flex;gap:0.75rem;">
        <input v-model="search" type="text" placeholder="Search staff..."
               style="flex:1;padding:0.5rem 0.9rem;border:1.5px solid rgba(26,61,43,0.15);border-radius:10px;outline:none;" />
        <button class="btn btn-forest" @click="fetchStaff">Search</button>
        <button class="btn btn-outline" @click="search=''; fetchStaff()">Clear</button>
      </div>
    </div>

    <!-- Table -->
    <div class="card" style="padding:0;overflow:hidden;">
      <div v-if="loading" class="empty-state"><p>Loading...</p></div>
      <div v-else-if="staffList.length === 0" class="empty-state">
        <h4>No staff found</h4>
      </div>
      <div v-else style="overflow-x:auto;">
        <table>
          <thead>
            <tr>
              <th>Staff Member</th>
              <th>Contact</th>
              <th>Experience</th>
              <th>Specialization</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in staffList" :key="s.id">
              <td>
                <div style="font-weight:600;">{{ s.name }}</div>
                <div style="font-size:0.78rem;color:#6c757d;">@{{ s.username }}</div>
              </td>
              <td style="font-size:0.85rem;">
                <div>{{ s.email }}</div>
                <div style="color:#6c757d;">{{ s.phone }}</div>
              </td>
              <td>{{ s.experience_years }}yr</td>
              <td style="font-size:0.82rem;">{{ s.specialization || '—' }}</td>
              <td>
                <span :class="`badge ${s.status === 'active' ? 'badge-open' : 'badge-closed'}`">
                  {{ s.status }}
                </span>
              </td>
              <td>
                <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">
                  <button class="btn btn-sm btn-outline" @click="openEdit(s)">Edit</button>
                  <button class="btn btn-sm"
                          :class="s.status === 'active' ? 'btn-ember' : 'btn-sage'"
                          @click="toggleStatus(s.id)">
                    {{ s.status === 'active' ? 'Blacklist' : 'Activate' }}
                  </button>
                  <button class="btn btn-sm btn-ember" @click="deleteStaff(s.id)">Del</button>
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
          {{ editStaff ? 'Edit Staff' : 'Add New Staff' }}
        </h5>
        <form @submit.prevent="saveStaff">
          <div class="grid-2">
            <div class="form-group">
              <label>Full Name *</label>
              <input v-model="form.name" required />
            </div>
            <div class="form-group">
              <label>Username *</label>
              <input v-model="form.username" :disabled="!!editStaff" required />
            </div>
            <div class="form-group">
              <label>Email *</label>
              <input v-model="form.email" type="email" required />
            </div>
            <div class="form-group">
              <label>Phone</label>
              <input v-model="form.phone" />
            </div>
            <div class="form-group">
              <label>{{ editStaff ? 'New Password' : 'Password *' }}</label>
              <input v-model="form.password" type="password"
                     :required="!editStaff" placeholder="Min 6 chars" />
            </div>
            <div class="form-group">
              <label>Experience (years)</label>
              <input v-model="form.experience_years" type="number" min="0" />
            </div>
            <div class="form-group" style="grid-column:1/-1;">
              <label>Specialization</label>
              <input v-model="form.specialization"
                     placeholder="e.g. High-altitude trekking, First Aid" />
            </div>
          </div>
          <div v-if="formError" class="alert alert-danger">{{ formError }}</div>
          <div style="display:flex;gap:0.75rem;margin-top:1rem;">
            <button type="submit" class="btn btn-forest">
              {{ editStaff ? 'Update' : 'Add Staff' }}
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
  name: 'AdminStaff',
  setup() {
    const staffList = ref([])
    const loading = ref(false)
    const showModal = ref(false)
    const editStaff = ref(null)
    const formError = ref(null)
    const search = ref('')

    const form = ref({
      name: '', username: '', email: '',
      phone: '', password: '',
      experience_years: 0, specialization: ''
    })

    const resetForm = () => {
      form.value = {
        name: '', username: '', email: '',
        phone: '', password: '',
        experience_years: 0, specialization: ''
      }
      formError.value = null
    }

    const fetchStaff = async () => {
      loading.value = true
      try {
        const res = await axios.get('/api/admin/staff', {
          params: search.value ? { search: search.value } : {}
        })
        staffList.value = res.data
      } catch (e) { console.error(e) }
      loading.value = false
    }

    const openEdit = (s) => {
      editStaff.value = s
      form.value = {
        name: s.name, username: s.username,
        email: s.email, phone: s.phone || '',
        password: '',
        experience_years: s.experience_years,
        specialization: s.specialization || ''
      }
      showModal.value = true
    }

    const saveStaff = async () => {
      formError.value = null
      try {
        if (editStaff.value) {
          await axios.put(`/api/admin/staff/${editStaff.value.id}`, form.value)
        } else {
          await axios.post('/api/admin/staff', form.value)
        }
        showModal.value = false
        resetForm()
        fetchStaff()
      } catch (e) {
        formError.value = e.response?.data?.errors?.join(', ')
          || e.response?.data?.error || 'Error saving'
      }
    }

    const toggleStatus = async (id) => {
      try {
        await axios.put(`/api/admin/staff/${id}/toggle_status`)
        fetchStaff()
      } catch (e) { console.error(e) }
    }

    const deleteStaff = async (id) => {
      if (!confirm('Delete this staff member?')) return
      try {
        await axios.delete(`/api/admin/staff/${id}`)
        fetchStaff()
      } catch (e) { console.error(e) }
    }

    onMounted(fetchStaff)

    return {
      staffList, loading, showModal, editStaff,
      form, formError, search,
      fetchStaff, openEdit, saveStaff,
      toggleStatus, deleteStaff, resetForm
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
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}
</style>
