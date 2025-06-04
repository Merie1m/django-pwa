from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfflineAssetViewSet


# 🔧 Création d’un routeur DRF (il va générer automatiquement les routes)
router = DefaultRouter()
router.register(r'offline-assets', OfflineAssetViewSet, basename='offlineasset')

# 🌐 Inclusion des routes du ViewSet dans le système de routing de Django
urlpatterns = [
   
    path('', include(router.urls)),
    
]
