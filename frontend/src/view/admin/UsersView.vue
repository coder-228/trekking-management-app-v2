<template>
  <div class="main">
    <div class="page-header">
      <h2>Manage Trekkers</h2>
    </div>

    <div class="card" style="margin-bottom:1rem;padding:1rem;">
      <div style="display:flex;gap:0.75rem;">
        <input v-model="search" type="text" placeholder="Search users..."
               style="flex:1;padding:0.5rem 0.9rem;border:1.5px solid rgba(26,61,43,0.15);border-radius:10px;outline:none;" />
        <button class="btn btn-forest" @click="fetchUsers">Search</button>
        <button class="btn btn-outline" @click="search=''; fetchUsers()">Clear</button>
      </div>
    </div>

    <div class="card" style="padding:0;overflow:hidden;">
      <div v-if="loading" class="empty-state"><p>Loading...</p></div>
      <div v-else-if="users.length === 0" class="empty-state">
        <h4>No users found</h4>
      </div>
      <div v-else style="overflow-x:auto;">
        <table>
          <thead>
            <tr>
              <th>User</th>
              <th>Contact</th>
              <th>Age</th>
              <th>Joined</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td>
                <div style="font-weight:600;">{{ u.name }}</div>
                <div style="font-size:0.78rem;color:#6c757d;">@{{ u.username }}</div>
              </td>
              <td style="font-size:0.85rem;">
                <div>{{ u.email }}</div>
                <div style="color:#6c757d;">{{ u.phone }}</div>
              </td>
              <td>{{ u.age || '—' }}</td>
              <td style="font-size:0.82rem;color:#6c757d;">{{ u.created_at }}</td>
              <td>
                <span :class="`badge ${u.status === 'active' ? 'badge-open' : 'badge-closed'}`">
                  {{ u.status }}
                </span>
              </td>
              <td>
                <button class="btn btn-sm"
                        :class="u.status === 'active' ? 'btn-ember' : 'btn-sage'"
                        @click="toggleStatus(u.id)">
                  {{ u.status === 'active' ? 'Blacklist' : 'Activate' }}
                </button>
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
  name: 'AdminUsers',
  setup() {
    const users = ref([])
    const loading = ref(false)
    const search = ref('')

    const fetchUsers = async () => {
      loading.value = true
      try {
        const res = await axios.get('/api/admin/users', {
          params: search.value ? { search: search.value } : {}
        })
        users.value = res.data
      } catch (e) { console.error(e) }
      loading.value = false
    }

    const toggleStatus = async (id) => {
      if (!confirm('Change user status?')) return
      try {
        await axios.put(`/api/admin/users/${id}/toggle_status`)
        fetchUsers()
      } catch (e) { console.error(e) }
    }

    onMounted(fetchUsers)
    return { users, loading, search, fetchUsers, toggleStatus }
  }
}
</script>