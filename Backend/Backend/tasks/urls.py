from django.urls import path

from tasks import views
from .views import create_task_view, read_task_view, find_task_view, update_task_view, delete_task_view

urlpatterns = [
    path("create/", create_task_view),
    path("read/", read_task_view),
    path("<int:task_id>/", find_task_view),
    path("<int:task_id>/update/", update_task_view),
    path("<int:task_id>/delete/", delete_task_view)
]
