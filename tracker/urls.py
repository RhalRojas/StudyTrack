from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("tasks/", views.task_list, name="task_list"),
    path("log/", views.log_session, name="log_session"),
]
