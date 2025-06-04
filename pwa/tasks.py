from celery import shared_task
from .models import OfflineAsset, PushSubscription
import requests
from pywebpush import webpush, WebPushException

# 🔹 Tâche 1 : Pré-cacher les fichiers PWA (OfflineAsset)
@shared_task
def precache_assets():
    """
    Cette tâche télécharge chaque URL enregistrée dans le modèle OfflineAsset
    pour forcer leur mise en cache par le service worker.
    """
    assets = OfflineAsset.objects.all()
    for asset in assets:
        try:
            # Simule une requête GET pour forcer le serveur à servir l'asset
            response = requests.get(asset.url, timeout=10)

            # Vérifie que le fichier est bien accessible (code HTTP 200)
            if response.status_code == 200:
                print(f"[✓] Asset '{asset.name}' précaché avec succès.")
            else:
                print(f"[!] Échec précaching '{asset.name}' (code {response.status_code})")

        except Exception as e:
            print(f"[✗] Erreur lors du précaching de '{asset.name}': {e}")


# 🔹 Tâche 2 : Envoyer des notifications push à tous les abonnés
@shared_task
def send_push_notification(title, message):
    """
    Cette tâche envoie une notification push contenant `title` et `message`
    à tous les abonnés enregistrés dans le modèle PushSubscription.
    """
    subscriptions = PushSubscription.objects.all()

    for sub in subscriptions:
        try:
            # Préparer les données du push
            payload = {
                "title": title,
                "body": message
            }

            # Envoi du push via webpush
            webpush(
                subscription_info={
                    "endpoint": sub.endpoint,
                    "keys": {
                        "p256dh": sub.p256dh,
                        "auth": sub.auth
                    }
                },
                data=json.dumps(payload),  # corps de la notification (JSON)
                vapid_private_key="chemin/vers/vapid_private.pem",  # à modifier selon ton chemin
                vapid_claims={
                    "sub": "mailto:ton.email@exemple.com"  # obligatoire pour l'identité
                }
            )

            print(f"[✓] Notification envoyée à {sub.endpoint}")

        except WebPushException as e:
            print(f"[✗] Erreur d'envoi à {sub.endpoint}: {e}")

        except Exception as e:
            print(f"[!] Autre erreur: {e}")
