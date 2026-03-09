from django.urls import path

from tasks import views
from .views import task_detail_view, tasks_view

urlpatterns = [
    path("tasks/", tasks_view),
    path("tasks/<int:task_id>/", task_detail_view)
]
