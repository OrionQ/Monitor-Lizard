from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('tag/', views.tag),
    path('host/', views.host),
]
