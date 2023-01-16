from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from oauth.utils import RefreshToken
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class AuthSerializer(serializers.Serializer):
    username = serializers.SlugField(write_only=True)
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def _validate_from_username(self, attrs):
        try:
            user = self._get_user_from_username(attrs)
            if not user.check_password(attrs.get('password')):
                raise ValidationError({'detail': _('Username или пароль не верно')})
        except User.DoesNotExist:
            raise ValidationError({'detail': _('Username или пароль не верно')})
        return attrs

    @staticmethod
    def _get_user_from_username(validated_data):
        return User.objects.get(username=validated_data['username'])

    def _get_user(self, validated_data):
        return self._get_user_from_username(validated_data)

    def validate(self, attrs):
        return self._validate_from_username(attrs)

    def create(self, validated_data):
        user = self._get_user(validated_data)
        token = RefreshToken().for_user(user)
        return {
            'access': str(token.access_token),
            'refresh': str(token)
        }
