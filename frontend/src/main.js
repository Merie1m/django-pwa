import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

// 🔐 Demander la permission de notification
//if ('Notification' in window && navigator.serviceWorker) {
 // Notification.requestPermission().then(permission => {
    //if (permission === 'granted') {
     // console.log("✅ Notifications autorisées !");
    //} else {
     // console.warn("🚫 Notifications refusées.");
    //}
 // });
//}
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(registration => {
        console.log('Service Worker registered with scope:', registration.scope);
      })
      .catch(error => {
        console.error('Service Worker registration failed:', error);
      });
  });
}
