from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products),
    path('customer/<str:pk_test>/', views.customer),
]
