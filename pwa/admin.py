from django.contrib import admin
from .models import OfflineAsset, PushSubscription,Project, Task, Comment, Notification


admin.site.register(Task)
admin.site.register(OfflineAsset)
admin.site.register(PushSubscription)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Notification)
