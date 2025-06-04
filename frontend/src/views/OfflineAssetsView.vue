<template>
  <div>
    <h2>Données Offline</h2>
    <div v-if="loading">Chargement...</div>
    <div v-else-if="!data">Aucune donnée</div>
    <ul v-else>
      <li v-for="item in data" :key="item.id">{{ item.nom }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      data: null,
      loading: true
    }
  },
  async mounted() {
    const token = localStorage.getItem('access_token')

    if (!token) {
      // Rediriger vers /login si pas connecté
      this.$router.push('/login')
      return
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/api/offline-assets/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        }
      })

      if (!response.ok) {
        throw new Error('Non autorisé')
      }

      const result = await response.json()
      this.data = result
    } catch (err) {
      console.error(err)
      this.$router.push('/login')
    } finally {
      this.loading = false
    }
  }
}
</script>
