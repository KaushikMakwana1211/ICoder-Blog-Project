from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # API to post a comment
    path('postComment', views.postComment, name='postComment'),
    
    path('', views.BlogHome, name='BlogHome'),
    path('<str:slug>', views.blogPost, name='blogPost'),
    
]
