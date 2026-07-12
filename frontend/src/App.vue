<template>
  <div id="app">
    <NavBar v-if="auth.isAuthenticated" />
    <router-view />
  </div>
</template>

<script>
import { useAuthStore } from './stores/auth'
import NavBar from './components/NavBar.vue'

export default {
  name: 'App',
  components: { NavBar },
  setup() {
    const auth = useAuthStore()
    return { auth }
  }
}
</script>

<style>
:root {
  --forest: #1a3d2b;
  --moss: #2d6a4f;
  --sage: #52b788;
  --mist: #b7e4c7;
  --snow: #f8fffe;
  --ember: #e76f51;
  --gold: #f4a261;
  --dark: #0d1f17;
  --card-radius: 16px;
  --shadow: 0 4px 24px rgba(26,61,43,0.12);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
  background: var(--snow);
  color: var(--dark);
  min-height: 100vh;
}

.card {
  background: white;
  border-radius: var(--card-radius);
  box-shadow: var(--shadow);
  padding: 1.5rem;
}

.btn {
  padding: 0.6rem 1.2rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.btn-forest {
  background: var(--forest);
  color: white;
}
.btn-forest:hover { background: var(--dark); }

.btn-sage {
  background: var(--sage);
  color: white;
}
.btn-sage:hover { background: var(--moss); }

.btn-ember {
  background: var(--ember);
  color: white;
}
.btn-ember:hover { background: #c1440e; }

.btn-outline {
  background: transparent;
  border: 2px solid var(--forest);
  color: var(--forest);
}
.btn-outline:hover { background: var(--forest); color: white; }

.btn-sm {
  padding: 0.35rem 0.8rem;
  font-size: 0.8rem;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge-easy { background: #d8f3dc; color: #1b4332; }
.badge-moderate { background: #fff3cd; color: #664d03; }
.badge-hard { background: #f8d7da; color: #58151c; }
.badge-open { background: #d8f3dc; color: #1b4332; }
.badge-closed { background: #f8d7da; color: #58151c; }
.badge-pending { background: #fff3cd; color: #664d03; }
.badge-approved { background: #cff4fc; color: #055160; }
.badge-completed { background: #e2d9f3; color: #4a235a; }
.badge-booked { background: #d8f3dc; color: #1b4332; }
.badge-cancelled { background: #f8d7da; color: #58151c; }

.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--forest);
  margin-bottom: 0.4rem;
}
.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.6rem 0.9rem;
  border: 1.5px solid rgba(26,61,43,0.15);
  border-radius: 10px;
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s;
}
.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: var(--sage);
}

.alert {
  padding: 0.75rem 1rem;
  border-radius: 10px;
  margin-bottom: 1rem;
  font-size: 0.88rem;
  border-left: 4px solid;
}
.alert-success { background: #d8f3dc; color: #1b4332; border-color: var(--sage); }
.alert-danger { background: #f8d7da; color: #58151c; border-color: var(--ember); }
.alert-warning { background: #fff3cd; color: #664d03; border-color: var(--gold); }

.page-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(26,61,43,0.08);
}
.page-header h2 {
  font-size: 1.6rem;
  color: var(--forest);
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}
.empty-state h4 { margin-top: 1rem; }

.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }

@media (max-width: 768px) {
  .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
}

table { width: 100%; border-collapse: collapse; }
th {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6c757d;
  padding: 0.75rem 1rem;
  border-bottom: 2px solid rgba(26,61,43,0.1);
  text-align: left;
  font-weight: 600;
}
td {
  padding: 0.85rem 1rem;
  border-bottom: 1px solid rgba(26,61,43,0.05);
  font-size: 0.88rem;
}
tr:hover td { background: rgba(82,183,136,0.04); }

.main { padding: 2rem; max-width: 1400px; margin: 0 auto; }
</style>
