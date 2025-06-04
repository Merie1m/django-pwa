from django.db import models
from django.core.validators import MinLengthValidator, URLValidator
from django.core.exceptions import ValidationError
from .crypto_utils import encrypt_data, decrypt_data
from django.contrib.auth.models import User
# Modèle représentant une ressource à mettre en cache pour une utilisation hors ligne
class OfflineAsset(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        help_text="Nom de la ressource, minimum 3 caractères."
    )
    url = models.URLField(
        unique=True,
        validators=[URLValidator()],
        help_text="URL unique vers la ressource (ex: /static/js/main.js)."
    )
    version = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(1)],
        help_text="Version de la ressource (ex: 'v1.0.3')."
    )
    file_type = models.CharField(
        max_length=20,
        choices=[
            ('image', 'Image'),
            ('script', 'Script'),
            ('style', 'Feuille de style'),
            ('html', 'HTML'),
            ('other', 'Autre')
        ],
        default='other',
        help_text="Type de ressource pour aider à la gestion du cache."
    )
    size_kb = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Taille approximative du fichier en kilo-octets."
    )
    is_critical = models.BooleanField(
        default=False,
        help_text="Cette ressource est-elle critique pour l'affichage hors ligne ?"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Met automatiquement la date de mise à jour à chaque modification."
    )

    def __str__(self):
        return f"{self.name} (v{self.version})"

    class Meta:
        verbose_name = "Ressource hors ligne"
        verbose_name_plural = "Ressources hors ligne"
        ordering = ['-updated_at']


# Modèle représentant un abonnement push pour envoyer des notifications Web
class PushSubscription(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    endpoint = models.URLField(
        unique=True,
        validators=[URLValidator()],
        help_text="URL d'envoi fournie par le navigateur lors de l'abonnement Web Push."
    )
    p256dh = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(10)],
        help_text="Clé publique du client (pour chiffrer les messages)."
    )
    auth = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(10)],
        help_text="Jeton d'authentification sécurisé."
    )
    browser = models.CharField(
        max_length=50,
        choices=[
            ('chrome', 'Chrome'),
            ('firefox', 'Firefox'),
            ('edge', 'Edge'),
            ('safari', 'Safari'),
            ('other', 'Autre')
        ],
        default='other',
        help_text="Le navigateur utilisé par l'utilisateur."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Si l'utilisateur a désactivé les notifications, passe à False."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date d'enregistrement initial de l'abonnement."
    )
    last_used = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Dernière fois où une notification a été envoyée."
    )

    def __str__(self):
        return f"{self.browser} - {self.endpoint[:30]}..."

    def clean(self):
        """Validation personnalisée des champs de sécurité."""
        if not self.endpoint.startswith("https://"):
            raise ValidationError("L'endpoint doit commencer par https://")
        if not self.p256dh or len(self.p256dh) < 10:
            raise ValidationError("Clé publique invalide ou trop courte.")
        if not self.auth or len(self.auth) < 10:
            raise ValidationError("Jeton d'authentification invalide ou trop court.")
    
    def save(self, *args, **kwargs):
        """
        Avant de sauvegarder, on chiffre les champs sensibles.
        On s'assure que les données ne sont pas déjà chiffrées (optionnel).
        """
        # Ici, on chiffre systématiquement (attention: si tu récupères un objet existant et le sauvegardes, double chiffrement possible)
       # self.endpoint = encrypt_data(self.endpoint)
        self.p256dh = encrypt_data(self.p256dh)
        self.auth = encrypt_data(self.auth)
        super().save(*args, **kwargs)

    def get_decrypted_keys(self):
        """
        Méthode pour obtenir les champs sensibles déchiffrés.
        Utile pour envoyer les notifications, etc.
        """
        return {
           # "endpoint": decrypt_data(self.endpoint),
            "p256dh": decrypt_data(self.p256dh),
            "auth": decrypt_data(self.auth),
        }
    class Meta:
        verbose_name = "Abonnement Push"
        verbose_name_plural = "Abonnements Push"
        ordering = ['-created_at']



class Project(models.Model):
    users = models.ManyToManyField(User, related_name='projects')  # plusieurs utilisateurs # propriétaire du projet
    name = models.CharField(
        max_length=100,
        unique=True,  # nom unique pour éviter les doublons
        validators=[MinLengthValidator(3)]  # au moins 3 caractères
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks')  # 🧑‍💻 Utilisateur créateur de la tâche
    title = models.CharField(max_length=100)  # 📝 Titre de la tâche
    description = models.TextField(blank=True, null=True)  # 📄 Description facultative
    status = models.CharField(  # ✅ État de la tâche
        max_length=20,
        choices=[
            ('todo', 'À faire'),
            ('in_progress', 'En cours'),
            ('done', 'Terminée')
        ],
        default='todo'
    )
    due_date = models.DateField(blank=True, null=True)  # 📅 Date limite (facultative)
    priority = models.IntegerField(default=1)  # 🔺 Priorité (1 = basse, 5 = urgente)

    created_at = models.DateTimeField(auto_now_add=True)  # 🕒 Créée le
    updated_at = models.DateTimeField(auto_now=True)      # 🔄 Mise à jour le

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.user.username} sur {self.project.name}"
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    content = models.TextField()  # texte de la notification
    is_read = models.BooleanField(default=False)  # pour savoir si la notif a été lue
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif pour {self.user.username} - {self.content[:30]}"
