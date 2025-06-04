from pywebpush import webpush, WebPushException
from vapid_keys import get_vapid_private_key_base64, get_vapid_public_key

def send_push(subscription_info, payload):
    """
    Envoie une notification push avec pywebpush en utilisant les clés VAPID.
    subscription_info : dict contenant endpoint et clés de l'abonnement push utilisateur
    payload : message à envoyer dans la notification
    """
    vapid_private_key = get_vapid_private_key_base64()
    vapid_claims = {
        "sub": "mailto:meriem.toumi@sesame.com.tn"
    }

    try:
        webpush(
            subscription_info=subscription_info,
            data=payload,
            vapid_private_key=vapid_private_key,
            vapid_claims=vapid_claims
        )
        print("✅ Notification envoyée avec succès")
    except WebPushException as e:
        print("❌ Erreur lors de l'envoi :", repr(e))

# Test manuel, exécuté seulement si on lance ce fichier directement
if __name__ == "__main__":
    subscription_info = {
        "endpoint": "https://fcm.googleapis.com/fcm/send/...",  # Remplace par vrai endpoint
        "keys": {
            "p256dh": "clé_publique_utilisateur",  # Remplace par vraie clé publique
            "auth": "clé_auth_utilisateur"         # Remplace par vraie clé auth
        }
    }

    send_push(subscription_info, "Ceci est un test de notification push ! 🎉")


# Ce script Python permet d'envoyer une notification push à un utilisateur
# qui a accepté de recevoir des notifications sur son navigateur.
#
# Fonctionnement général :
# 1. Côté client (navigateur) :
#    - L'utilisateur donne la permission de recevoir des notifications.
#    - Le navigateur crée un "abonnement push" (subscription_info) contenant un
#      endpoint unique et des clés (p256dh, auth).
#    - Ce subscription_info est envoyé à ton serveur/backend.
#
# 2. Côté serveur (ce script) :
#    - Le serveur reçoit le subscription_info de l'utilisateur.
#    - Il utilise la clé privée VAPID pour s'authentifier auprès du service push.
#    - Il envoie la notification à l'endpoint du navigateur via la fonction webpush().
#
# 3. Côté client (navigateur) :
#    - Le service worker reçoit la notification et l'affiche à l'utilisateur,
#      même si la page web est fermée.
#
# En résumé, ce script envoie une notification uniquement aux utilisateurs qui ont
# accepté de recevoir des notifications et qui ont envoyé leur abonnement push
# au serveur.