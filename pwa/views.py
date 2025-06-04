# Import des vues génériques basées sur les modèles pour créer des APIs automatiquement
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
# Import des modèles définis précédemment
from .models import OfflineAsset, PushSubscription
from django.http import FileResponse, Http404
# Import des serializers qui transforment les objets en JSON (et inversement)
from .serializers import OfflineAssetSerializer, PushSubscriptionSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import PushSubscription
  
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.views import APIView
from .models import OfflineAsset
from .serializers import OfflineAssetSerializer

from django.http import JsonResponse
import json
import os
from django.conf import settings
from rest_framework import filters
from django.http import HttpResponse
from django.views.decorators.cache import never_cache

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import permission_classes, authentication_classes

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
  
   
    # Vérifier que le username n'existe pas déjà
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Vérifier que l'email n'existe pas déjà (optionnel mais recommandé)
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Créer l'utilisateur avec create_user pour gérer correctement le password
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

@never_cache
def service_worker(request):
    path = os.path.join('pwa', 'public', 'sw.js')  # 👈 nouveau chemin
    try:
        return FileResponse(open(path, 'rb'), content_type='application/javascript')
    except FileNotFoundError:
        raise Http404("Service worker file not found")

class OfflineAssetViewSet(viewsets.ModelViewSet):
    queryset = OfflineAsset.objects.all()
    serializer_class = OfflineAssetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['version']
    @action(detail=False, methods=['get'])
    def critical(self, request):
        critical_assets = OfflineAsset.objects.filter(is_critical=True)
        serializer = self.get_serializer(critical_assets, many=True)
        return Response(serializer.data)

class PushSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = PushSubscription.objects.all()
    serializer_class = PushSubscriptionSerializer
    permission_classes = [IsAuthenticated]  # Exige que l'utilisateur soit authentifié
    #permission_classes = [AllowAny] 
   
    def perform_create(self, serializer):
        # Exemple : assigner l'utilisateur courant à l'abonnement
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def active(self, request):
        # Retourner uniquement les abonnements actifs de l'utilisateur connecté
        user = request.user
        active_subs = PushSubscription.objects.filter(user=user, is_active=True)
        serializer = self.get_serializer(active_subs, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Exemple : interdire la suppression si abonnement actif
        instance = self.get_object()
        if instance.is_active:
            return Response({"detail": "Impossible de supprimer un abonnement actif."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
  

    @action(detail=False, methods=['get'], url_path='decrypted')
    def decrypted_subscriptions(self, request):
        user = request.user
        subs = PushSubscription.objects.filter(user=user, is_active=True)
        data = [sub.get_decrypted_keys() for sub in subs]
        return Response(data)
    

    
class TaskViewset(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)


  #manifest
def manifest(request):
    manifest_data = {
        "name": "Mon Application PWA",
        "short_name": "MonApp",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#000000",
        "icons": [
            {
                "src": "/static/icons/icon1.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/icons/icon-512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }
    return JsonResponse(manifest_data)

