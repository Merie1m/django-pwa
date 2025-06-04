# Imports
import graphene
from graphene_django import DjangoObjectType
from .models import OfflineAsset, PushSubscription
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
# Enums
class BrowserEnum(graphene.Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    SAFARI = "safari"
    OTHER = "other"

# Types GraphQL
class OfflineAssetType(DjangoObjectType):
    class Meta:
        model = OfflineAsset

class PushSubscriptionType(DjangoObjectType):
    class Meta:
        model = PushSubscription

# Mutations OfflineAsset
class CreateOfflineAsset(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        url = graphene.String(required=True)
        version = graphene.String(required=True)
        file_type = graphene.String(required=True)
        size_kb = graphene.Int(required=True)
        is_critical = graphene.Boolean(required=True)

    offline_asset = graphene.Field(OfflineAssetType)

    def mutate(self, info, name, url, version, file_type, size_kb, is_critical):
        asset = OfflineAsset.objects.create(
            name=name,
            url=url,
            version=version,
            file_type=file_type,
            size_kb=size_kb,
            is_critical=is_critical,
        )
        return CreateOfflineAsset(offline_asset=asset)

class UpdateOfflineAsset(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        url = graphene.String()
        version = graphene.String()
        file_type = graphene.String()
        size_kb = graphene.Int()
        is_critical = graphene.Boolean()

    offline_asset = graphene.Field(OfflineAssetType)

    def mutate(self, info, id, **kwargs):
        try:
            asset = OfflineAsset.objects.get(pk=id)
            for attr, value in kwargs.items():
                setattr(asset, attr, value)
            asset.save()
            return UpdateOfflineAsset(offline_asset=asset)
        except OfflineAsset.DoesNotExist:
            raise Exception("OfflineAsset not found")

class DeleteOfflineAsset(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            asset = OfflineAsset.objects.get(pk=id)
            asset.delete()
            return DeleteOfflineAsset(success=True)
        except OfflineAsset.DoesNotExist:
            return DeleteOfflineAsset(success=False)


def is_valid_url(url):
    validator = URLValidator()
    try:
        validator(url)
        return True
    except ValidationError:
        return False


# Mutations PushSubscription
class CreatePushSubscription(graphene.Mutation):
    class Arguments:
        endpoint = graphene.String(required=True)
        p256dh = graphene.String(required=True)
        auth = graphene.String(required=True)
        browser = graphene.Argument(BrowserEnum, required=True)
        is_active = graphene.Boolean(required=True)
        # Ne PAS mettre user ici

    push_subscription = graphene.Field(PushSubscriptionType)

    def mutate(self, info, endpoint, p256dh, auth, browser, is_active):
        user = info.context.user  # à l’intérieur de mutate
        if user.is_anonymous:
            raise Exception("Authentification requise")

        if not is_valid_url(endpoint):
            raise Exception("URL de l'endpoint invalide")

        subscription = PushSubscription.objects.create(
            endpoint=endpoint,
            p256dh=p256dh,
            auth=auth,
            browser=browser.value,
            is_active=is_active,
            user=user,  # ici seulement
        )

        return CreatePushSubscription(push_subscription=subscription)


class UpdatePushSubscription(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        endpoint = graphene.String()
        p256dh = graphene.String()
        auth = graphene.String()
        browser = graphene.String()
        is_active = graphene.Boolean()

    push_subscription = graphene.Field(PushSubscriptionType)

    def mutate(self, info, id, **kwargs):
        push_subscription = PushSubscription.objects.get(pk=id)
        for key, value in kwargs.items():
            setattr(push_subscription, key, value)
        push_subscription.save()
        return UpdatePushSubscription(push_subscription=push_subscription)

class DeletePushSubscription(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            subscription = PushSubscription.objects.get(pk=id)
            subscription.delete()
            return DeletePushSubscription(success=True)
        except PushSubscription.DoesNotExist:
            return DeletePushSubscription(success=False)

# Root Types
class Query(graphene.ObjectType):
    offline_assets = graphene.List(OfflineAssetType)
    push_subscriptions = graphene.List(PushSubscriptionType)
    
    #sync_status = graphene.Field(SyncStatusType) 
    is_offline_ready = graphene.Boolean()


    def resolve_offline_assets(root, info):
        return OfflineAsset.objects.all()

    def resolve_push_subscriptions(root, info):
        return PushSubscription.objects.all()


    def resolve_is_offline_ready(root, info):
        return OfflineAsset.objects.exists()
    
"""class SyncStatusType(graphene.ObjectType):
    asset_count = graphene.Int()
    latest_version = graphene.String()
"""


class Mutation(graphene.ObjectType):
    create_offline_asset = CreateOfflineAsset.Field()
    update_offline_asset = UpdateOfflineAsset.Field()
    delete_offline_asset = DeleteOfflineAsset.Field()
    create_push_subscription = CreatePushSubscription.Field()
    update_push_subscription = UpdatePushSubscription.Field()
    delete_push_subscription = DeletePushSubscription.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)