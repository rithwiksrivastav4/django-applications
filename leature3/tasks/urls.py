from django.urls import path # type: ignore
from . import views


app_name = "tasks"
urlpatterns = [
    path("",views.tasks_view , name = "task"),
    path("add/",views.add, name = "add"),
    path("delete/", views.delete, name="delete"),
]


