from django.urls import path

from accounts import views
from .views import login_view, refresh_token_view, logout_view, register_view

urlpatterns = [
    path("login/", login_view),
    path("refresh/", refresh_token_view),
    path("logout/", logout_view),
    path("register/", register_view)
]
