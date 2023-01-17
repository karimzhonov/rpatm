from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.contrib.auth import get_user_model
from .tabulers import UserOutstandingTokenTabuler


User = get_user_model()
admin.site.unregister(User)

@admin.register(User)
class UserAdmin(_UserAdmin):
    inlines = []
