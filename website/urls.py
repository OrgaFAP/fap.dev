from django.urls import path
from . import views

urlpatterns = [
    path("", views.index2, name="index2"),
    path("donate/", views.donate, name="donate"),
    path("architecture/", views.analyse, name="analyse"),
    path("ressource/", views.ressource, name="ressource"),
    path("thoughts/", views.thoughts, name="thoughts"),
    path("explore/", views.why, name="why"),
    path("how-data/", views.how_data, name="how_data"),
]
