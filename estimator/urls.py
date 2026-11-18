from django.urls import path

from . import views

app_name = "estimator"

urlpatterns = [
    path("healthz/", views.health, name="health"),
    path("api/home-pay/", views.home_pay, name="home_pay"),
]
