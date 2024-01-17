from django.urls import path
from . import views
from .views import update_order_notes
from .views import job_search_results
from .views import update_job_notes
from .views import job_list
from .views import create_job
from .views import add_part_to_job
from .views import update_job_machine
from .views import search_parts_ajax

urlpatterns = [
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:sage_order_number>/', views.order_detail, name='order_detail'),
    path('customer_orders/<int:customer_id>/', views.customer_orders, name='customer_orders'),
    path('order_detail/<int:sage_order_number>/', views.order_detail, name='order_detail'),
    path('job/<str:job_id>/', views.job_detail, name='job_detail'),
    path('update_order_notes/', update_order_notes, name='update_order_notes'),
    path('job-search-results/', job_search_results, name='job_search_results'),
    path('jobs/', views.job_list, name='job_list'),
    path('update_job_notes/', views.update_job_notes, name='update_job_notes'),
    path('jobs/search/', job_list, name='job_search'),
    path('jobs/create/', create_job, name='create_job'),
    path('add-part-to-job/', add_part_to_job, name='add_part_to_job'),
    path('remove_part_from_job/', views.remove_part_from_job, name='remove_part_from_job'),
    path('update-job-machine/', update_job_machine, name='update_job_machine'),
    path('jobs/update-machine/<int:job_id>/', update_job_machine, name='update_job_machine'),
    path('ajax/search-parts/', search_parts_ajax, name='search_parts_ajax'),
 

    

    # Example: path('orders/', views.order_list, name='order_list'),
    # Add more URL patterns for other views in your app
]
