from django.urls import path

from web.controllers import views, host_endpoints

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
    path('tag/<str:tag_id>/', views.tag, name="tag"),
    path('host/<str:host_id>/', views.host, name="host"),
    path('host/<str:host_id>/containers/', views.containers),
    path('host/<str:host_id>/processes/', views.processes),
]
