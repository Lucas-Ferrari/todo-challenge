from django.urls import path
from .views import TaskList, TaskView


urlpatterns = [
    path("list/", TaskList.as_view(), name="tasks_list"),
    path("get_by_id/", TaskView.as_view(), name="tasks_get_by_id"),
    path("create/", TaskView.as_view(), name="tasks_create"),
    path("update/", TaskView.as_view(), name="tasks_update"),
]
