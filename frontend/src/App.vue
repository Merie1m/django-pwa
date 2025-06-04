<template>
  <div>
    <!-- ---j'ai ajouté ici: navbar--- -->
    <nav class="navbar">
      <ul>
        <li><router-link to="/login">Login</router-link></li>
        <li><router-link to="/tasks">Tasks</router-link></li>
        <li><router-link to="/register">Register</router-link></li>
      </ul>
    </nav>
    <!-- ---fin ajout navbar--- -->

    <header class="navbar">
      <h1>📢 Mon Application de Notifications</h1>
    </header>

    <main class="content">
      <router-view />
    </main>

    <footer class="footer">
      <p>&copy; 2025 Mon App</p>
    </footer>
  </div>
</template>

<script>
export default {
  methods: {
    logout() {
      localStorage.removeItem('token'); // supprime le token
      this.$router.push('/login');      // redirige vers la page login
    }
  }
}
</script>


<style scoped>
/* ---j'ai ajouté ici: style navbar --- */
.navbar {
  background-color: #42b983;
  padding: 1rem;
  color: white;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar ul {
  list-style: none;
  display: flex;
  justify-content: center;
  gap: 2rem;
  padding: 0;
  margin: 0;
}

.navbar ul li a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.navbar ul li a.router-link-exact-active {
  text-decoration: underline;
}

.navbar ul li a:hover {
  text-decoration: underline;
}
/* ---fin style navbar--- */

.content {
  padding: 2rem;
  min-height: 70vh;
}

.footer {
  background-color: #f5f5f5;
  padding: 1rem;
  text-align: center;
  color: #555;
  font-size: 0.9rem;
  border-top: 1px solid #ddd;
}
</style>
