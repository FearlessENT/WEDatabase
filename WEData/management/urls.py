from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.order_list, name='order_list'),
    # Example: path('orders/', views.order_list, name='order_list'),
    # Add more URL patterns for other views in your app
]
