from rest_framework import serializers
from .models import OfflineAsset, PushSubscription,Task


class OfflineAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineAsset
        fields = '__all__'

    def validate_url(self, value):
        if not (
            value.startswith("https://") or
            value.startswith("http://") or
            value.startswith("/")
        ):
            raise serializers.ValidationError(
                "L'URL doit commencer par '/', 'http://' ou 'https://'"
            )
        return value

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Le nom doit contenir au moins 3 caractères.")
        return value

    def validate(self, data):
        return data


class PushSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushSubscription
        
        fields = ['id', 'endpoint', 'auth', 'p256dh', 'created_at']

    def validate_endpoint(self, value):
        if not value.startswith("https://"):
            raise serializers.ValidationError("L'endpoint doit commencer par 'https://'.")
        return value

    def validate_p256dh(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("La clé publique est trop courte.")
        return value

    def validate_auth(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Le jeton d'authentification est trop court.")
        return value

    def validate(self, data):
        # Validation globale (optionnelle)
        # Par exemple, vérifier que endpoint et p256dh sont compatibles ou autres règles complexes
        return data
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'