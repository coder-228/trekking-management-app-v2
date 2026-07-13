<template>
  <div class="main" style="max-width:700px;">
    <div class="page-header">
      <h2>My Profile</h2>
    </div>

    <div class="grid-2" style="align-items:start;">
      <!-- Profile Summary -->
      <div class="card" style="text-align:center;">
        <div class="avatar-lg">{{ auth.userName?.charAt(0).toUpperCase() }}</div>
        <h5 style="font-weight:700;margin:0.75rem 0 0.25rem;">{{ profile.name }}</h5>
        <div style="color:#6c757d;font-size:0.88rem;">@{{ profile.username }}</div>
        <span class="badge badge-open" style="margin-top:0.5rem;">Active Trekker</span>
        <hr style="margin:1rem 0;border-color:rgba(26,61,43,0.08);">
        <div style="text-align:left;">
          <div style="font-size:0.82rem;color:#6c757d;margin-bottom:0.5rem;">
            ✉️ {{ profile.email }}
          </div>
          <div v-if="profile.phone"
               style="font-size:0.82rem;color:#6c757d;margin-bottom:0.5rem;">
            📱 {{ profile.phone }}
          </div>
          <div v-if="profile.age"
               style="font-size:0.82rem;color:#6c757d;margin-bottom:0.5rem;">
            👤 Age: {{ profile.age }}
          </div>
          <div style="font-size:0.82rem;color:#6c757d;">
            📅 Since {{ profile.created_at }}
          </div>
        </div>

        <!-- Export CSV -->
        <hr style="margin:1rem 0;border-color:rgba(26,61,43,0.08);">
        <button class="btn btn-outline" style="width:100%;" @click="exportCSV">
          📥 Export Booking History
        </button>
        <div v-if="exportMsg" class="alert alert-success" style="margin-top:0.75rem;">
          {{ exportMsg }}
        </div>
      </div>

      <!-- Edit Form -->
      <div class="card">
        <h6 style="font-weight:700;color:var(--forest);margin-bottom:1rem;">
          Edit Profile
        </h6>
        <form @submit.prevent="saveProfile">
          <div class="form-group">
            <label>Full Name *</label>
            <input v-model="form.name" required />
          </div>
          <div class="form-group">
            <label>Phone</label>
            <input v-model="form.phone" />
          </div>
          <div class="form-group">
            <label>Age</label>
            <input v-model="form.age" type="number" min="10" max="100" />
          </div>
          <div class="form-group">
            <label>Emergency Contact</label>
            <input v-model="form.emergency_contact" placeholder="Parent / Spouse name" />
          </div>
          <div class="form-group">
            <label>Emergency Phone</label>
            <input v-model="form.emergency_phone" />
          </div>

          <hr style="border-color:rgba(26,61,43,0.08);margin:1rem 0;">
          <h6 style="font-size:0.82rem;color:#6c757d;margin-bottom:0.75rem;">
            Change Password (leave blank to keep)
          </h6>
          <div class="form-group">
            <label>New Password</label>
            <input v-model="form.new_password" type="password" placeholder="Min 6 chars" />
          </div>
          <div class="form-group">
            <label>Confirm Password</label>
            <input v-model="form.confirm_password" type="password" />
          </div>

          <div v-if="saveError" class="alert alert-danger">{{ saveError }}</div>
          <div v-if="saveSuccess" class="alert alert-success">{{ saveSuccess }}</div>

          <button type="submit" class="btn btn-forest" style="width:100%;">
            Save Changes
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import axios from 'axios'

export default {
  name: 'UserProfile',
  setup() {
    const auth = useAuthStore()
    const profile = ref({})
    const saveError = ref(null)
    const saveSuccess = ref(null)
    const exportMsg = ref(null)

    const form = ref({
      name: '', phone: '', age: '',
      emergency_contact: '', emergency_phone: '',
      new_password: '', confirm_password: ''
    })

    const fetchProfile = async () => {
      try {
        const res = await axios.get('/api/user/profile')
        profile.value = res.data
        form.value.name = res.data.name
        form.value.phone = res.data.phone || ''
        form.value.age = res.data.age || ''
        form.value.emergency_contact = res.data.emergency_contact || ''
        form.value.emergency_phone = res.data.emergency_phone || ''
      } catch (e) { console.error(e) }
    }

    const saveProfile = async () => {
      saveError.value = null
      saveSuccess.value = null
      try {
        await axios.put('/api/user/profile', form.value)
        saveSuccess.value = 'Profile updated!'
        fetchProfile()
      } catch (e) {
        saveError.value = e.response?.data?.error || 'Update failed'
      }
    }

    const exportCSV = async () => {
      try {
        const res = await axios.post('/api/user/export')
        exportMsg.value = res.data.message
      } catch (e) { console.error(e) }
    }

    onMounted(fetchProfile)
    return { auth, profile, form, saveError, saveSuccess, exportMsg, saveProfile, exportCSV }
  }
}
</script>

<style scoped>
.avatar-lg {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: var(--sage);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0 auto;
}
</style>