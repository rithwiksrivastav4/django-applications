from django.urls import path # pyright: ignore[reportMissingModuleSource]
from . import views

urlpatterns = [
    path("", views.index , name = "index"),
    path("show/",views.name, name= "names"),
    path("<str:name>", views.greet, name = "greet"),
    path("sri/", views.srivastav , name = "sriastav")
    
              ]