<template>
  <nav class="navbar">
    <router-link to="/">Accueil</router-link>
    <router-link to="/login">Login</router-link>
    <router-link to="/register">Register</router-link>
    <router-link to="/tasks">Tasks</router-link>
  </nav>
</template>

<script>
export default {
  name: 'Navbar'
}
</script>

<style scoped>
.navbar {
  background-color: #333;
  padding: 1em;
}
.navbar a {
  color: white;
  margin-right: 1em;
  text-decoration: none;
}
.navbar a.router-link-exact-active {
  font-weight: bold;
  text-decoration: underline;
}
</style>
