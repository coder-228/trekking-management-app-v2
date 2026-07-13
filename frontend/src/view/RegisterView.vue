<template>
  <div class="login-page">
    <div class="login-card card">
      <div class="login-header">
        <div class="login-icon">▲</div>
        <h1>Join SummitQuest</h1>
        <p>Start your trekking journey today</p>
      </div>
      <form @submit.prevent="handleRegister">
        <div class="grid-2">
          <div class="form-group">
            <label>Full Name *</label>
            <input v-model="form.name" type="text" placeholder="John Muir" required />
          </div>
          <div class="form-group">
            <label>Username *</label>
            <input v-model="form.username" type="text" placeholder="johnmuir" required />
          </div>
          <div class="form-group">
            <label>Email *</label>
            <input v-model="form.email" type="email" placeholder="john@example.com" required />
          </div>
          <div class="form-group">
            <label>Phone</label>
            <input v-model="form.phone" type="tel" placeholder="+91 9876543210" />
          </div>
          <div class="form-group">
            <label>Password *</label>
            <input v-model="form.password" type="password" placeholder="Min 6 chars" required />
          </div>
          <div class="form-group">
            <label>Age</label>
            <input v-model="form.age" type="number" placeholder="25" />
          </div>
        </div>
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <div v-if="success" class="alert alert-success">{{ success }}</div>

        <button type="submit" class="btn btn-forest w-full" :disabled="loading">
          {{ loading ? 'Creating...' : 'Create Account' }}
        </button>
      </form>
      <div class="login-footer">
        <p>Already have an account? <router-link to="/login">Sign in</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
export default {
  name: 'RegisterView',
  setup() {
    const auth = useAuthStore()
    const router = useRouter()

    const form = ref({
      name: '', username: '', email: '',
      phone: '', password: '', age: ''
    })
    const loading = ref(false)
    const error = ref(null)
    const success = ref(null)

    const handleRegister = async () => {
      loading.value = true
      error.value = null
      success.value = null

      const result = await auth.register(form.value)
      if (result.success) {
        success.value = 'Registration successful! Redirecting to login...'
        setTimeout(() => router.push('/login'), 1500)
      } else {
        error.value = result.error
      }

      loading.value = false
    }

    return { form, loading, error, success, handleRegister }
  }
}
</script>
<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0d1f17, #1a3d2b, #2d6a4f);
  padding: 2rem 1rem;
}

.login-card {
  width: 100%;
  max-width: 560px;
}
.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-icon { font-size: 2rem; color: var(--sage); }

.login-header h1 {
  font-size: 1.8rem;
  color: var(--forest);
  font-weight: 900;
}
.login-header p { color: #6c757d; font-size: 0.88rem; }

.w-full { width: 100%; margin-top: 0.5rem; }
.login-footer {
  text-align: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(26,61,43,0.08);
}

.login-footer a {
  color: var(--moss);
  font-weight: 600;
  text-decoration: none;
}
</style>
