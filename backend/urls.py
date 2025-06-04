from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from pwa.views import OfflineAssetViewSet, PushSubscriptionViewSet
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from pwa.schema import schema
from pwa.views import service_worker
from pwa import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from pwa.views import TaskViewset
from rest_framework.views import APIView
from django.urls import path






router = routers.DefaultRouter()
router.register(r'offline-assets', OfflineAssetViewSet)
router.register(r'push-subscriptions', PushSubscriptionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('sw.js', service_worker, name='service_worker'),
    path('manifest.json', views.manifest, name='manifest'),
    path('api/', include('pwa.urls')),  # routes API de ton app PWA
    path('manifest.json', views.manifest, name='manifest'),
    path('register/', views.register, name='register'),
   
    # Route pour générer les tokens (login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Route pour rafraîchir un access token expiré
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Inclure les routes de ton app si ce n’est pas déjà fait
    path('api/', include('pwa.urls')),  # adapte le nom de l'app si différent
    #path('protected/',views.protected_view, name='protected'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('api/tasks/', TaskViewset.as_view({'get': 'list'}), name='task-list'),
  
]
