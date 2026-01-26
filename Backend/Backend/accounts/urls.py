from django.urls import path

from accounts import views
from .views import login_view, signIn_view, check_login_view

urlpatterns = [
    path("login/", login_view),
    path("signin/", signIn_view),
    path("check/", check_login_view)
]
