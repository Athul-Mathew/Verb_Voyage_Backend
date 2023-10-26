from django.contrib import admin
from .models  import *
# Register your models here.
admin.site.register(Mentor)
admin.site.register(Playlist)
admin.site.register(Video)
admin.site.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user','verb','is_read']
