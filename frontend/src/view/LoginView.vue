<template>
  <div class="login-page">
    <div class="login-card card">
      <div class="login-header">
        <div class="login-icon">▲</div>
        <h1>SummitQuest</h1>
        <p>Sign in to continue your adventure</p>
      </div>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Username / Email</label>
          <input
            v-model="form.username"
            type="text"
            placeholder="Enter username"
            required
          />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="Enter password"
            required
          />
        </div>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <button type="submit" class="btn btn-forest w-full" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>
      <div class="login-footer">
        <p>New trekker? <router-link to="/register">Create account</router-link></p>
        <p class="hint">Admin: admin / admin123</p>
      </div>
    </div>
  </div>
</template>
<script>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'LoginView',
  setup() {
    const auth = useAuthStore()
    const router = useRouter()

    const form = ref({ username: '', password: '' })
    const loading = ref(false)
    const error = ref(null)

    const handleLogin = async () => {
      loading.value = true
      error.value = null

      const result = await auth.login(form.value.username, form.value.password)

      if (result.success) {
        router.push(`/${result.role}/dashboard`)
      } else {
        error.value = result.error
      }

      loading.value = false
    }

    return { form, loading, error, handleLogin }
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
}

.login-card {
  width: 100%;
  max-width: 400px;
  margin: 1rem;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-icon {
  font-size: 2rem;
  color: var(--sage);
  margin-bottom: 0.5rem;
}

.login-header h1 {
  font-size: 1.8rem;
  color: var(--forest);
  font-weight: 900;
}

.login-header p {
  color: #6c757d;
  font-size: 0.88rem;
  margin-top: 0.25rem;
}
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
.hint {
  font-size: 0.78rem;
  color: #aaa;
  margin-top: 0.5rem;
}
</style>
