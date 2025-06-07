from django.contrib import admin
from django import forms
from django.forms.widgets import PasswordInput
from .models import OfflineAsset, PushSubscription, Project, Task, Comment, Notification


class PushSubscriptionForm(forms.ModelForm):
    class Meta:
        model = PushSubscription
        fields = '__all__'
        widgets = {
            'p256dh': PasswordInput(render_value=True),
            'auth': PasswordInput(render_value=True),
        }


@admin.register(PushSubscription)
class PushSubscriptionAdmin(admin.ModelAdmin):
    form = PushSubscriptionForm  # ← CETTE LIGNE EST IMPORTANTE !
    list_display = ("user", "browser", "is_active", "created_at", "short_p256dh", "short_auth")
    readonly_fields = ("short_p256dh", "short_auth")
    
    # Grouper les champs dans des fieldsets pour une meilleure organisation
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user', 'browser', 'is_active')
        }),
        ('Configuration Push', {
            'fields': ('endpoint', 'p256dh', 'auth'),
            'description': 'Les clés sont masquées pour la sécurité'
        }),
        ('Dates', {
            'fields': ('created_at', 'last_used'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'short_p256dh', 'short_auth')

    def short_p256dh(self, obj):
        return "••••••••" if obj.p256dh else ""
    short_p256dh.short_description = "P256dh"

    def short_auth(self, obj):
        return "••••••••" if obj.auth else ""
    short_auth.short_description = "Auth"


# Vos autres modèles
admin.site.register(Task)
admin.site.register(OfflineAsset)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Notification)