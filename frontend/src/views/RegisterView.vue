// Après l'inscription réussie, on affiche un bouton pour que l'utilisateur
// puisse s'abonner aux notifications push.
// Quand il clique sur ce bouton, on demande la permission de notifications,
// on crée un abonnement push (subscription_info) qui contient :
// - un endpoint unique : c'est une URL spécifique qui identifie le navigateur de l'utilisateur,
//   où le serveur enverra la notification push,
// - deux clés de chiffrement (p256dh et auth) : utilisées pour sécuriser la communication
//   entre le serveur et le navigateur.
// Ensuite, on envoie cet abonnement au backend pour pouvoir lui envoyer des notifications plus tard.

<template>
  <div style="max-width: 500px; margin: 2rem auto; padding: 2rem; border: 1px solid #eee; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <h2 style="color: #2c3e50; margin-bottom: 1.5rem;">Inscription</h2>
    <form @submit.prevent="register">
      <input v-model="name" placeholder="Nom" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Mot de passe" required />
      <button type="submit">S'inscrire</button>
    </form>

    <div v-if="error" style="color:red">{{ error }}</div>

    <!-- ✅ Affiché si inscription réussie -->
      <div v-if="showSubscribeButton">
      <p>Inscription réussie !</p>
      <button @click="subscribeToPush">S'abonner aux notifications</button>
    </div>
  </div>
</template>

<script>
import { subscribeToPush } from '../pushNotifications.js' 

export default {
  data() {
    return {
      name: '',
      email: '',
      password: '',
      error: '',
      showSubscribeButton: false
    }
  },
  methods: {
    async register() {
      try {
        const response = await fetch('http://127.0.0.1:8000/register/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.name,
            email: this.email,
            password: this.password
          })
        });

        if (!response.ok) {
          let err = 'Erreur lors de l’inscription';
          try {
            const json = await response.json();
            err = json.message || JSON.stringify(json);
          } catch {}
          this.error = err;
          return;
        }

        // Affiche le bouton s'abonner aux notifications (ne pas rediriger ici)
        this.showSubscribeButton = true;
      } catch (e) {
        this.error = 'Erreur réseau';
      }
    },

    subscribeToPush() {
      subscribeToPush();
    }
  }
}
</script>
  

}