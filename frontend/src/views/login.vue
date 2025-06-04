<template>
  <div>
    <h2>Login simple</h2>
    <form @submit.prevent="submitLogin">
      <label>Nom d'utilisateur :</label>
      <input type="text" v-model="username" required />
      <label>Mot de passe :</label>
      <input type="password" v-model="password" required />
      <button type="submit">Se connecter</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      message: ''
    }
  },
  methods: {
    async submitLogin() {
      this.message = ''
      try {
        const response = await fetch('http://127.0.0.1:8000/api/token/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        })

        if (!response.ok) {
          throw new Error('Identifiants invalides')
        }

        const data = await response.json()

       localStorage.setItem('token', data.access); // 🛠️ change 'access_token' → 'token'
       this.message = 'Connexion réussie ! Token stocké.'
await new Promise(r => setTimeout(r, 1000))  // pause 1s
console.log("this.$router =", this.$router)
this.$router.push({ path: '/tasks' })
      } catch (err) {
        this.message = err.message
      }
     
    }
  }
}
</script>