# 🛰️ PWA Sync & Push Backend – Django + DRF + GraphQL

Ce projet fournit une API robuste pour la gestion des fonctionnalités PWA côté serveur, incluant la synchronisation offline, les notifications push, la sécurité des endpoints, et des tâches asynchrones avec Celery. Il s'intègre avec Django, Django REST Framework (DRF), GraphQL (graphene-django) et Celery pour une architecture moderne et scalable.

## 📦 Fonctionnalités principales

✅ **1. Gestion des assets offline (OfflineAsset)**  
Stockage des ressources nécessaires au fonctionnement hors-ligne (manifestes, scripts, styles…).  
Contraintes d’intégrité (unicité, format d’URL, accessibilité).

✅ **2. Abonnement aux notifications push (PushSubscription)**  
Sauvegarde sécurisée des abonnements (endpoint, clés).  
Validation stricte des endpoints et des clés (VAPID).

✅ **3. API REST & GraphQL**  
DRF ViewSets pour la création, la lecture et la suppression des abonnements et assets.  
GraphQL mutations/queries :  
- Enregistrement de l’abonnement push  
- Récupération des assets offline  
- Suivi de la synchronisation utilisateur

✅ **4. Sécurité**  
Authentification par token (JWT ou OAuth2).  
Chiffrement des clés push stockées.  
Protection CSRF & CORS.

✅ **5. Tâches asynchrones avec Celery**  
Pré-chargement automatique des assets pour les nouveaux utilisateurs.  
Envoi de notifications push en tâche planifiée.  
Traitement des logs d’usage via une tâche AI d’analyse prédictive.
