from django.urls import path

from . import views

app_name = "estimator"

urlpatterns = [path("healthz/", views.health, name="health")]
