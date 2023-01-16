from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import AuthSerializer


class AuthView(CreateAPIView):
    serializer_class = AuthSerializer
    authentication_classes = ()
    permission_classes = ()


class RefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer
    permission_classes = ()
    authentication_classes = ()
