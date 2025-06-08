
Description du Projet
Ce projet implémente une Progressive Web App complète avec Django, incluant la gestion des assets hors ligne, les notifications push, et la synchronisation des données. Le système utilise Django REST Framework et GraphQL pour les API, avec une architecture sécurisée pour la gestion des clés de chiffrement.
Modèles de Données
OfflineAsset
Le modèle OfflineAsset gère les ressources disponibles hors ligne 

Fonctionnalités :
Stockage des métadonnées des assets
Validation de la taille (doit être positive)
Contrainte d'unicité sur URL + version
Marquage des assets critiques

PushSubscription
Le modèle PushSubscription gère les abonnements aux notifications push :

Fonctionnalités :
Association user-endpoint unique
Chiffrement des clés sensibles (p256dh et auth)
Gestion du statut actif/inactif
Validation des endpoints push
Authentification et Sécurité
JWT Authentication
Le projet utilise l'authentification JWT pour sécuriser les endpoints :
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

Chiffrement des Clés Push
Les clés VAPID et les clés d'authentification sont chiffrées avant stockage :
# Fonctions de chiffrement/déchiffrement
def encrypt_key(key_data):
    """Chiffre une clé avec Fernet"""
    cipher_suite = Fernet(settings.ENCRYPTION_KEY)
    return cipher_suite.encrypt(key_data.encode()).decode()

def decrypt_key(encrypted_key):
    """Déchiffre une clé avec Fernet"""
    cipher_suite = Fernet(settings.ENCRYPTION_KEY)
    return cipher_suite.decrypt(encrypted_key.encode()).decode()

Configuration requise :
Variable d'environnement ENCRYPTION_KEY pour Fernet
Clés VAPID publique et privée pour les notifications push
Validation des endpoints avec pywebpush
API REST
Endpoints Disponibles
Assets Hors Ligne
GET /api/assets/
POST /api/assets/
PUT /api/assets/{id}/
DELETE /api/assets/{id}/


Abonnements Push
GET /api/push-subscriptions/
POST /api/push-subscriptions/
GET /api/push-subscriptions/decrypted/
DELETE /api/push-subscriptions/{id}/


Service Worker
GET /sw.js

Retourne le service worker avec la logique de mise en cache et de synchronisation. 
Fonctionnalités PWA Hors Ligne
Gestion de l'Authentification Hors Ligne
Grâce au service worker, l'application offre une expérience utilisateur complète même sans connexion internet :
Interfaces Disponibles Hors Ligne :
Interface de connexion (login)
Interface d'inscription (register)
interface qui affiche la liste des taches 
interface qui affiche la liste des projet
(on peut faire crud aussi hors ligne mais je n’ai pas touvé le temps de l’ajouter)
Mécanisme d'Inscription Différée : Lorsqu'un utilisateur tente de s'inscrire en mode hors ligne, le processus suit cette logique :
Les données d'inscription sont automatiquement sauvegardées dans le cache du service worker
Une fois la connexion internet rétablie, les données sont synchronisées automatiquement
L'utilisateur est alors effectivement enregistré dans la base de données backend
Accès aux Données Utilisateur Hors Ligne
Pour les utilisateurs authentifiés, le service worker permet l'accès complet aux données personnelles en mode hors ligne :
Liste des projets de l'utilisateur
Liste des tâches associées à chaque projet
Navigation fluide entre les différentes sections
Notifications Push Hors Ligne
Le service worker prend en charge l'envoi de notifications push même en mode hors ligne, avec la possibilité de :
Tester les notifications via les DevTools du navigateur
Maintenir la communication avec l'utilisateur sans connexion activ
Validation des Données
Tous les endpoints incluent une validation robuste :
Endpoints Push : Validation du format URL et de la structure des clés
Assets : Validation du content-type et de la taille
Manifestes : Validation de la structure JSON selon les standards PWA
API GraphQL
Queries Disponibles
type Query {
    # Statut de synchronisation
    syncStatus: SyncStatusType
    
    # Assets hors ligne
    offlineAssets: [OfflineAssetType]
    
    # Abonnements push de l'utilisateur
    myPushSubscriptions: [PushSubscriptionType]
}

Mutations Disponibles
type Mutation {
    # Gestion des assets
    createOfflineAsset(input: OfflineAssetInput!): CreateOfflineAssetMutation
    updateOfflineAsset(id: ID!, input: OfflineAssetInput!): UpdateOfflineAssetMutation
    deleteOfflineAsset(id: ID!): DeleteOfflineAssetMutation
    
    # Gestion des abonnements push
    createPushSubscription(input: PushSubscriptionInput!): CreatePushSubscriptionMutation
    deletePushSubscription(id: ID!): DeletePushSubscriptionMutation
    
    # Synchronisation
    syncOfflineData: SyncOfflineDataMutation
}

Types GraphQL
type OfflineAssetType {
    id: ID!
    url: String!
    contentType: String!
    size: Int!
    version: String!
    isCritical: Boolean!
    lastModified: DateTime!
}

type PushSubscriptionType {
    id: ID!
    endpoint: String!
    createdAt: DateTime!
    isActive: Boolean!
}

type SyncStatusType {
    lastSync: DateTime
    pendingCount: Int!
    isOnline: Boolean!
}

Service Worker
Fonctionnalités Implémentées
Le service worker (/sw.js) inclut :
Cache Strategy

 // Cache-first pour les assets critiques
// Network-first pour les données dynamiques
// Stale-while-revalidate pour les ressources statiques


Background Sync

 self.addEventListener('sync', event => {
    if (event.tag === 'offline-sync') {
        event.waitUntil(syncOfflineData());
    }
});


Push Notifications

 self.addEventListener('push', event => {
    const data = event.data.json();
    self.registration.showNotification(data.title, data.options);
});

Notifications Push
Configuration VAPID
# test_vapid.py
from pywebpush import webpush, WebPushException

# Test des clés VAPID
vapid_private_key = "votre_cle_privee"
vapid_public_key = "votre_cle_publique"

# Envoi de notification de test
def send_test_notification(subscription_info):
    try:
        webpush(
            subscription_info=subscription_info,
            data="Test notification",
            vapid_private_key=vapid_private_key,
            vapid_claims={"sub": "mailto:contact@example.com"}
        )
        print("✅ Notification envoyée avec succès")
    except WebPushException as ex:
        print(f"❌ Erreur: {ex}")

Endpoint de Déchiffrement
L'endpoint /api/push-subscriptions/decrypted/ permet de récupérer les clés déchiffrées pour les tests :
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_decrypted_subscriptions(request):
    subscriptions = PushSubscription.objects.filter(user=request.user)
    decrypted_data = []
    
    for sub in subscriptions:
        decrypted_data.append({
            'endpoint': sub.endpoint,
            'keys': {
                'p256dh': decrypt_key(sub.p256dh_key),
                'auth': decrypt_key(sub.auth_key)
            }
        })
    
    return Response(decrypted_data)

Installation et Configuration

3. Configuration
# Variables d'environnement (.env)
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://user:pass@localhost/dbname
ENCRYPTION_KEY=your_fernet_key
VAPID_PRIVATE_KEY=your_vapid_private_key
VAPID_PUBLIC_KEY=your_vapid_public_key

4. Base de Données
# Migrations
python manage.py makemigrations pwa
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

5. Génération des Clés
# Générer une clé Fernet
from cryptography.fernet import Fernet
encryption_key = Fernet.generate_key()
print(encryption_key.decode())

# Générer des clés VAPID
from pywebpush import vapid
vapid_keys = vapid.vapid_gen()
print("Private Key:", vapid_keys['privateKey'])
print("Public Key:", vapid_keys['publicKey'])

Tests





Tests Manuels
Service Worker : Vérifier dans DevTools > Application > Service Workers
Cache : Inspecter le cache dans DevTools > Application > Storage
Notifications : Tester avec l'endpoint de notification de test
Hors ligne : Désactiver le réseau et vérifier le fonctionnement
État du Projet
✅ Fonctionnalités Complètes
Modèles avec contraintes - OfflineAsset et PushSubscription implémentés
Validation - Endpoints push et manifestes validés
API REST/GraphQL - Sérialiseurs et types GraphQL complets
Endpoints REST - Service worker enregistré, assets et abonnements disponibles
GraphQL - Queries de statut et mutations de synchronisation
Sécurité - JWT configuré, chiffrement des clés implémenté
🟡 Améliorations Possibles
Service Worker - Logique minimale, peut être enrichie



