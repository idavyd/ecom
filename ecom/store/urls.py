from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('product/<int:pk>', views.product_view, name='product'),
    path('category/<str:foo>', views.category_view, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_info/', views.update_info, name='update_info'),
    path('search/', views.search, name='search')
]