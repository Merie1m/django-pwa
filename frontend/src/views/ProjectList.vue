<template>
  <div>
    <h2>Liste des projets</h2>
    <ul>
      <li v-for="p in projects" :key="p.id" class="project-item">
        <h3>{{ p.name }}</h3>
        <p><strong>Description :</strong> {{ p.description || 'Pas de description' }}</p>
      </li>
    </ul>
    
  </div>
</template>

<script>
export default {
  data() {
    return {
      projects: []
    }
  },
  mounted() {
    this.loadProjects();
  },
  methods: {
    loadProjects() {
      const token = localStorage.getItem("token");
      if (!token) {
        this.$router.push("/login");
        return;
      }

      fetch("http://localhost:8000/api/projects/", {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        if (res.status === 401) throw new Error("Token expiré");
        if (!res.ok) throw new Error("Erreur de chargement");
        return res.json();
      })
      .then(data => {
        this.projects = data;
        localStorage.setItem("projects_cache", JSON.stringify(data));
      })
      .catch(err => {
        console.warn("Erreur de fetch, tentative depuis cache :", err.message);
        const cached = localStorage.getItem("projects_cache");
        if (cached) {
          this.projects = JSON.parse(cached);
        } else {
          alert("Impossible de charger les projets");
        }
      });
    }
  }
}
</script>

<style scoped>
.project-item {
  border: 1px solid #ccc;
  padding: 12px;
  margin-bottom: 12px;
  border-radius: 6px;
  background-color: #eef6ff;
}
.project-item h3 {
  margin: 0 0 8px;
}
</style>
