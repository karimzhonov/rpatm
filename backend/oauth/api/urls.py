from django.urls import path

from .views import AuthView, RefreshView

urlpatterns = [
    path('auth/', AuthView.as_view()),
    path('refresh-token/', RefreshView.as_view()),
]
