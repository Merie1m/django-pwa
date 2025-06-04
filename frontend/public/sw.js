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
  '/Images/logo.png'    // Logo de l'application
];

// 📥 Installation du Service Worker
self.addEventListener('install', event => {
  // ⏳ Attend que tous les fichiers soient ajoutés au cache
  event.waitUntil(
    caches.open(CACHE_NAME)                 // 📂 Ouvre (ou crée) le cache nommé CACHE_NAME
      .then(cache => cache.addAll(urlsToCache)) // ➕ Ajoute tous les fichiers listés dans urlsToCache
  );
});

// 🌐 Interception des requêtes réseau
self.addEventListener('fetch', event => {
  // 🔍 Si l’URL contient '/api/tasks/', c’est une requête API dynamique
  if (event.request.url.includes('/api/tasks/')) {
    // 📦 Réponse avec stratégie "network first, fallback cache"
    event.respondWith(
      caches.open(DATA_CACHE_NAME).then(cache => // 📂 Ouvre le cache DATA_CACHE_NAME
        fetch(event.request)                      // 🌐 Essaie de faire la requête réseau
          .then(response => {
            // ✅ Si la requête réussit (code 200), on met une copie dans le cache
            if (response.status === 200) {
              cache.put(event.request.url, response.clone()); // 🧾 Sauvegarde la réponse dans le cache
            }
            return response; // ↩️ Retourne la réponse réseau au client
          })
          .catch(() => {
            // ❌ En cas d’échec réseau, on tente de répondre avec le cache
            return cache.match(event.request); // 🔄 Fallback : réponse depuis cache si dispo
          })
      )
    );
    return; // 🚫 Stop ici, ne pas exécuter le code en dessous
  }

  // 📦 Pour toutes les autres requêtes (ex : fichiers statiques)
  event.respondWith(
    caches.match(event.request)       // 🔍 Cherche si la requête est déjà en cache
      .then(response => response || fetch(event.request)) // ↩️ Si oui, renvoie-la sinon va la chercher en réseau
  );
});

// 🔔 Réception d'une notification push
self.addEventListener('push', function(event) {
  let data = {}; // 📦 Objet qui va contenir les données de la notification

  try {
    // ✅ Essaie de récupérer les données envoyées au format JSON
    data = event.data ? event.data.json() : {};
  } catch (e) {
    // ⚠️ Si erreur (pas du JSON), essaie de lire le texte brut
    data = { title: event.data.text() };
  }

  const title = data.title || 'Notification'; // 🏷️ Titre par défaut si non fourni
  const options = {
    body: data.body || '',                   // 📝 Corps (texte) de la notification
    icon: data.icon || '/favicon.ico',       // 🖼️ Icône de la notification
    badge: data.badge || '/favicon.ico'      // 🎖️ Petit badge pour certains appareils
  };

  // 🧨 Affiche la notification avec le titre et les options
  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});
