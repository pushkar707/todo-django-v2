from django.urls import path
from core.views import RegisterApi, LoginApi, RefreshApi

urlpatterns = [
    path('register/', RegisterApi.as_view()),
    path('login/', LoginApi.as_view()),
    path('refresh/', RefreshApi.as_view())
]
