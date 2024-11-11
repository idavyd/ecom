from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.home_view, name='home'),
]