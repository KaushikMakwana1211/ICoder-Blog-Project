from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('signup/', views.handaleSignUp, name='handaleSignUp'),
    path('login/', views.handaleLogin, name='handaleLogin'),
    path('logout/', views.handaleLogout, name='handaleLogout'),
]
