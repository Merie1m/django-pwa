import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/login.vue'
import TaskList from '../views/TaskList.vue'
import ProjectList from '../views/ProjectList.vue'
import HelloWorld from '../components/HelloWorld.vue'
import RegisterView from '../views/RegisterView.vue'

const routes = [
  { 
    path: '/', 
    name: 'Home',           // ← Ajout du name
    component: HelloWorld 
  },
  { 
    path: '/login', 
    name: 'Login',          // ← Ajout du name
    component: Login 
  },
  { 
    path: '/tasks', 
    name: 'Tasks',          // ← Ajout du name
    component: TaskList 
  },
  { 
    path: '/projects', 
    name: 'Projects',       
    component: ProjectList 
  },
  { 
    path: '/register', 
    name: 'Register',       // ← Ajout du name
    component: RegisterView 
  },
]

// Suppression du bloc vide { }

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router