<template>
  <div>
    <h2>Liste des tâches</h2>
    
    <ul>
      <li v-for="task in tasks" :key="task.id" class="task-item">
        <h3>{{ task.title }}</h3>
        <p><strong>Description :</strong> {{ task.description || 'Pas de description' }}</p>
        <p><strong>Statut :</strong> {{ formatStatus(task.status) }}</p>
        <p><strong>Date limite :</strong> {{ task.due_date ? formatDate(task.due_date) : 'Aucune' }}</p>
        <p><strong>Priorité :</strong> {{ task.priority }}</p>
      </li>
    </ul>
   
  </div>

</template>

<script>
// Ajouter cette logique pour gérer le mode offline
export default {
  data() {
    return {
      tasks: [],
      isOnline: navigator.onLine
    };
  },
  created() {
    // Vérifier la connexion
    window.addEventListener('online', this.updateOnlineStatus);
    window.addEventListener('offline', this.updateOnlineStatus);
    
    // Charger les tâches
    this.loadTasks();
  },
  methods: {
    updateOnlineStatus() {
      this.isOnline = navigator.onLine;
    },
    async loadTasks() {
      if (this.isOnline) {
        // Mode online - requête au backend
        const response = await fetch('/api/tasks/');
        this.tasks = await response.json();
      } else {
        // Mode offline - utiliser le cache
        const cache = await caches.open('data-cache-v1');
        const cachedResponse = await cache.match('/api/tasks/');
        if (cachedResponse) {
          this.tasks = await cachedResponse.json();
        }
      }
    }
  }
};
</script>

<style scoped>
.task-item {
  border: 1px solid #ccc;
  padding: 12px;
  margin-bottom: 12px;
  border-radius: 6px;
  background-color: #f9f9f9;
}
.task-item h3 {
  margin: 0 0 8px;
}
</style>