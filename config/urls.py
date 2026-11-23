from django.urls import include, path

urlpatterns = [path("", include("estimator.urls"))]

handler500 = "estimator.views.server_error"
