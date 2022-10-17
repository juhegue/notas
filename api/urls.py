# -*- coding: utf-8 -*-

from django.urls import path
from api import views

# from rest_framework.authtoken.views import obtain_auth_token
# se ha sobreecrito para que contemple la caducidad del token
from .authtoken.views import obtain_auth_token


urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('login/', obtain_auth_token, name='api_login'),
    path('token_fcm/', views.TokenFcmView.as_view(), name='token_fcm'),
]