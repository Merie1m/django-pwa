import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/login.vue'
import TaskList from '../views/TaskList.vue'
import ProjectList from '../views/ProjectList.vue'
import HelloWorld from '../components/HelloWorld.vue'
import RegisterView from '../views/RegisterView.vue'
const routes = [
  { path: '/', component: HelloWorld },
  { path: '/login', component: Login },
  { path: '/tasks', component: TaskList },
   { path: '/projects', component: ProjectList },
  { path: '/register', component: RegisterView },


]

{
  

}
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
