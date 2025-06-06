// 🔒 Nom du cache principal pour les fichiers statiques
const CACHE_NAME = 'my-app-cache-v1';

// 🔒 Nom du cache pour les données dynamiques (ex : réponses API)
const DATA_CACHE_NAME = 'data-cache-v1';

// 📦 Liste des fichiers statiques à mettre en cache
const urlsToCache = [
  '/',                  // Page d'accueil
  '/index.html',        // Fichier HTML principal
  '/favicon.ico',       // Icône du site
  '/manifest.json',     // Fichier manifest pour PWA
  '/Images/logo.png',   // Logo de l'application
  '/tasks',             // Route tasks
  '/src/main.js',
]

// 📥 Installation du Service Worker
self.addEventListener('install', event => {
  console.log('Service Worker: Installation en cours...');
  
  // ⏳ Attend que tous les fichiers soient ajoutés au cache
  event.waitUntil(
    caches.open(CACHE_NAME)                 // 📂 Ouvre (ou crée) le cache nommé CACHE_NAME
      .then(cache => {
        console.log('Service Worker: Mise en cache des fichiers statiques');
        return cache.addAll(urlsToCache);   // ➕ Ajoute tous les fichiers listés dans urlsToCache
      })
      .catch(err => {
        console.error('Service Worker: Erreur lors de la mise en cache:', err);
      })
  );
});

// 🔄 Activation du Service Worker
self.addEventListener('activate', event => {
  console.log('Service Worker: Activation');
  
  // 🧹 Nettoie les anciens caches si nécessaire
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME && cacheName !== DATA_CACHE_NAME) {
            console.log('Service Worker: Suppression ancien cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// 🌐 Interception des requêtes réseau
// Ajouter cette stratégie de cache pour les routes
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Retourne la réponse en cache ou fetch si online
        return response || fetch(event.request);
      })
      .catch(() => {
        // Pour les routes spécifiques comme /tasks
        if (event.request.url.includes('/tasks')) {
          return caches.match('/tasks');
        }
      })
  );
});

// 🔔 Réception d'une notification push
self.addEventListener('push', function(event) {
  console.log('Service Worker: Notification push reçue');
  
  let data = {}; // 📦 Objet qui va contenir les données de la notification

  try {
    // ✅ Essaie de récupérer les données envoyées au format JSON
    data = event.data ? event.data.json() : {};
  } catch (e) {
    // ⚠️ Si erreur (pas du JSON), essaie de lire le texte brut
    data = { title: event.data ? event.data.text() : 'Notification' };
  }

  const title = data.title || 'Notification'; // 🏷️ Titre par défaut si non fourni
  const options = {
    body: data.body || '',                   // 📝 Corps (texte) de la notification
    icon: data.icon || '/favicon.ico',       // 🖼️ Icône de la notification
    badge: data.badge || '/favicon.ico',     // 🎖️ Petit badge pour certains appareils
    tag: data.tag || 'default',              // 🏷️ Tag pour grouper les notifications
    requireInteraction: false,               // 🔔 La notification disparaît automatiquement
    actions: data.actions || []              // 🎯 Actions possibles sur la notification
  };

  // 🧨 Affiche la notification avec le titre et les options
  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// 👆 Gestion du clic sur les notifications
self.addEventListener('notificationclick', function(event) {
  console.log('Service Worker: Clic sur notification');
  
  event.notification.close(); // 🚫 Ferme la notification

  // 🌐 Ouvre ou focus la fenêtre de l'application
  event.waitUntil(
    clients.matchAll().then(function(clientList) {
      // Si une fenêtre est déjà ouverte, la met au premier plan
      for (let i = 0; i < clientList.length; i++) {
        let client = clientList[i];
        if (client.url === '/' && 'focus' in client) {
          return client.focus();
        }
      }
      // Sinon, ouvre une nouvelle fenêtre
      if (clients.openWindow) {
        return clients.openWindow('/');
      }
    })
  );
});

// 📊 Gestion des erreurs du Service Worker
self.addEventListener('error', function(event) {
  console.error('Service Worker: Erreur détectée:', event.error);
});

// 🔄 Gestion des erreurs non capturées
self.addEventListener('unhandledrejection', function(event) {
  console.error('Service Worker: Promise rejetée non gérée:', event.reason);
});

console.log('Service Worker: Chargé et prêt !');

// Ajouter cette stratégie de cache pour les données utilisateur
self.addEventListener('fetch', event => {
  // Gérer les requêtes API pour les tâches
  if (event.request.url.includes('/api/tasks/')) {
    event.respondWith(
      caches.open(DATA_CACHE_NAME).then(cache => {
        return fetch(event.request)
          .then(response => {
            // Mettre en cache la réponse pour usage offline
            cache.put(event.request, response.clone());
            return response;
          })
          .catch(() => {
            // Retourner les données en cache si offline
            return cache.match(event.request);
          });
      })
    );
  }
});