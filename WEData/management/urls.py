from django.urls import path
from . import views
from .views import update_order_notes

urlpatterns = [
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:sage_order_number>/', views.order_detail, name='order_detail'),
    path('customer_orders/<int:customer_id>/', views.customer_orders, name='customer_orders'),
    path('order_detail/<int:sage_order_number>/', views.order_detail, name='order_detail'),
    path('job/<str:job_id>/', views.job_detail, name='job_detail'),
    path('update_order_notes/', update_order_notes, name='update_order_notes'),

    # Example: path('orders/', views.order_list, name='order_list'),
    # Add more URL patterns for other views in your app
]
