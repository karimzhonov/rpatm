from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

User = get_user_model()


class UserOutstandingToken(OutstandingToken):
    DEVICES_IDS = [
        [0, "Desktop"],
        [1, "Android"],
        [2, "iOS"],
        [3, "Mobile WEB"],
    ]

    device_id = models.IntegerField(choices=DEVICES_IDS, default=0)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    mac_address = models.CharField(max_length=128, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'token_blacklist_outstandingtoken'
        verbose_name = _('User Auth Table')
        verbose_name_plural = _('User Auth Tables')
