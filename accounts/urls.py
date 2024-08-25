from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.loginView, name='login'),
    path('login_success/', views.login_success, name='login_success'),
    path('logout/', views.logoutView, name='logout'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('reset_password/<uidb64>/<token>/',
         views.reset_password, name='reset_password'),

]
