from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("resources/", views.resource_list, name="resource_list"),
    path("resources/<int:id>/", views.resource_detail, name="resource_detail"),
    path("favorites/", views.favorites_view, name="favorites"),
    path("preferences/", views.preferences, name="preferences"),
    path("feedback/", views.feedback, name="feedback"),
    path("feedback/thanks/", views.feedback_thanks, name="feedback_thanks"),
]