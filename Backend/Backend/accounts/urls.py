from django.urls import path

from accounts import views
from .views import login_view, signIn_view

urlpatterns = [
    path("login/", login_view),
    path("signin/", signIn_view),
]
