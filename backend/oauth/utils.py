from oauth.models import UserOutstandingToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken as _RefreshToken
from rest_framework_simplejwt.utils import datetime_from_epoch


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class RefreshToken(_RefreshToken):

    @classmethod
    def for_user(cls, user, request=None):
        user_id = getattr(user, api_settings.USER_ID_FIELD)
        if not isinstance(user_id, int):
            user_id = str(user_id)

        token = cls()
        token[api_settings.USER_ID_CLAIM] = user_id

        device_id = 0
        user_ip = None
        user_agent = None
        if request:
            device_id = int(request.META.get('HTTP_X_DEVICE_ID', 0))
            user_ip = get_client_ip(request)
            user_agent = request.META['HTTP_USER_AGENT']

        UserOutstandingToken.objects.create(
            user=user,
            jti=token[api_settings.JTI_CLAIM],
            token=str(token),
            created_at=token.current_time,
            expires_at=datetime_from_epoch(token['exp']),
            device_id=device_id,
            ip_address=user_ip,
            mac_address=None,
            user_agent=user_agent,
            user_id=user_id
        )
        return token


class OnlyShowPermissionMixin:
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False