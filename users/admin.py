from datetime import timezone

from django.contrib import admin
from .models import UserModel, EmailVerificationModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    fields = (
    'username', 'first_name', 'last_name', ('email', 'email_verified'), 'phone', 'date_birth', 'date_joined', 'last_edited')
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_joined',)
    readonly_fields = ('date_joined', 'date_birth', 'last_edited',)


@admin.register(EmailVerificationModel)
class EmailVerificationModelAdmin(admin.ModelAdmin):
    fields = ('user', 'code', ('created_at', 'expires'),)
    list_display = ('user', 'created_at', 'expires',)
    readonly_fields = ('created_at',)

    def delete_model(self, request, obj):
        if obj.expires < timezone.now():
            obj.delete()
