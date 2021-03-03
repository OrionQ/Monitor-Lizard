from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
    path('tag/', views.tag, name="tag"),
    path('host/', views.host, name="host"),
    path('host/containers/', views.containers),
    path('host/processes/', views.processes),
]
