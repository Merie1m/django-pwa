<template>
  <div>
    <h2>Liste des Projets</h2>
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
export default {
  data() {
    return {
      tasks: []
    }
  },
  mounted() {
    this.loadTasks();
  },
  methods: {
    loadTasks() {
      const token = localStorage.getItem("token");
      if (!token) {
        this.$router.push("/login");
        return;
      }

      fetch("http://localhost:8000/api/tasks/", {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        if (res.status === 401) throw new Error("Token expiré");
        if (!res.ok) throw new Error("Erreur de chargement");
        return res.json();
      })
      .then(data => {
        this.tasks = data;
        localStorage.setItem("tasks_cache", JSON.stringify(data));
      })
      .catch(err => {
        console.warn("Erreur de fetch, tentative depuis cache :", err.message);
        const cached = localStorage.getItem("tasks_cache");
        if (cached) {
          this.tasks = JSON.parse(cached);
        } else {
          alert("Impossible de charger les tâches");
        }
      });
    },
    formatStatus(status) {
      const map = {
        'todo': 'À faire',
        'in_progress': 'En cours',
        'done': 'Terminée'
      };
      return map[status] || status;
    },
    formatDate(dateStr) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateStr).toLocaleDateString('fr-FR', options);
    }
  }
}
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
