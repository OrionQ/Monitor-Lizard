from django.urls import path

from web.controllers import host_endpoints

urlpatterns = [
    path('host/', host_endpoints.register),
]
