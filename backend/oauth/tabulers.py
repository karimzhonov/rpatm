from django.contrib import admin
from .models import UserOutstandingToken
from .utils import OnlyShowPermissionMixin

class UserOutstandingTokenTabuler(OnlyShowPermissionMixin, admin.TabularInline):
    model = UserOutstandingToken
    ordering = ['updated_at']
    fields = ['user', 'ip_address']
