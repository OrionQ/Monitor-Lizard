from django.urls import path

from web.controllers import views, host_endpoints

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
    path('tag/<str:tag_test>/', views.tag, name="tag"),
    path('host/<str:host_test>/', views.host, name="host"),
    path('host/<str:host_test>/containers/', views.containers),
    path('host/<str:host_test>/processes/', views.processes),
]
