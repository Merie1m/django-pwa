// Ce fichier permet au navigateur de s'abonner aux notifications push
// et d'envoyer cet abonnement au backend pour qu’il puisse plus tard envoyer des notifications ciblées


// Cette fonction permet d’abonner un utilisateur aux notifications push
export async function subscribeToPush() {
  // Vérifie que le navigateur supporte les notifications et les service workers
  if (!('Notification' in window) || !('serviceWorker' in navigator)) {
    alert("Push notifications ne sont pas supportées par ce navigateur.");
    return;
  }

  // Demande la permission à l’utilisateur pour recevoir des notifications
  const permission = await Notification.requestPermission();
  if (permission !== "granted") {
    alert("Permission refusée pour les notifications.");
    return;
  }

  try {
    // Attend que le Service Worker soit actif et prêt
    const registration = await navigator.serviceWorker.ready;

    // Définit les options pour l’abonnement push, notamment la clé publique VAPID
    const subscribeOptions = {
      userVisibleOnly: true, // Oblige une notification visible à l'utilisateur
      applicationServerKey: urlBase64ToUint8Array(
        "BFpFdb9CidGYwsRL0i3bHkIXrV0cLi81RBxvjEaazhxzShRKc-FmLwYPHHrQ0k4JKK-BP2khuJbyYw09VKQqS-g"
      )
    };

    // Demande au navigateur de s’abonner via le PushManager du Service Worker
    const pushSubscription = await registration.pushManager.subscribe(subscribeOptions);

    // Envoie les infos d’abonnement au backend (Django REST API)
    const response = await fetch('http://127.0.0.1:8000/api/push-subscriptions/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(pushSubscription)
    });

    // Vérifie si le backend a bien reçu l’abonnement
    if (!response.ok) {
      throw new Error("Erreur lors de l'envoi de l'abonnement au serveur");
    }

    // Message de succès
    alert("Abonnement aux notifications réussi !");
  } catch (err) {
    // Gestion des erreurs
    console.error("Erreur lors de l’abonnement push :", err.message || err);
    alert("Erreur lors de l’abonnement aux notifications : " + (err.message || err));
  }
}

// Cette fonction convertit une clé publique VAPID (base64) en tableau d’octets (Uint8Array)
// requis pour l'API Push (format attendu par applicationServerKey)
function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}
