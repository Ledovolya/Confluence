from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.conf.urls.static import static
from db import views

urlpatterns = [
    path('test_yadro/', views.test_yadro),
    path('confluence/', views.confluence_server_imitation),
]