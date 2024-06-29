from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_email_verified','profile_picture',)

    def profile_picture(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.profile_image.url))
        else:
            return 'None'