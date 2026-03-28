from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('signup/', views.register),
    path('signup.html', views.register),
    path('login/', views.user_login, name='login'),
    path('login.html', views.user_login),
    path('logout/', views.user_logout, name='logout'),
]
