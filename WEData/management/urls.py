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
from .views import cnc_operator_jobs
from .views import CustomLoginView
from .views import update_machine_notes
from django.contrib.auth import views as auth_views
from .views import update_machine_stage
from .views import update_job_mm8_stage
from .views import update_job_mm18_stage
from .views import picking_department
from .views import assembly_department
from .views import minikitchen_department
from .views import plywood_department


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
    path('cnc-operator-jobs/', cnc_operator_jobs, name='cnc-operator-jobs'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('update_machine_notes/', update_machine_notes, name='update_machine_notes'),
    path('update-machine-stage/', update_machine_stage, name='update_machine_stage'),
    path('machining/cnc_operator_jobs/', views.cnc_operator_jobs, name='cnc_operator_jobs'),
    path('update-job-mm8-stage/', update_job_mm8_stage, name='update_job_mm8_stage'),
    path('update-job-mm18-stage/', update_job_mm18_stage, name='update-job-mm18-stage'),
    path('picking/picking_department/', picking_department, name='picking_department'),
    path('update_picking_status/', views.update_picking_status, name='update_picking_status'),
    path('update_picking_notes/<int:picking_id>/', views.update_picking_notes, name='update_picking_notes'),
    path('assembly/assembly_department/', assembly_department, name='assembly_department'),
    path('update_assembly_notes/', views.update_assembly_notes, name='update_assembly_notes'),
    path('upholstery/upholstery_department/', views.upholstery_department, name='upholstery_department'),
    path('assembly/update_comments/', views.update_assembly_comments, name='update_assembly_comments'),
    path('update-assembly-status/', views.update_assembly_status, name='update_assembly_status'),
    path('management/update-workshop-notes/<int:workshop_id>/', views.update_workshop_notes, name='update_workshop_notes'),
    path('assembly/minikitchen_department/', minikitchen_department, name='minikitchen_department'),
    path('assembly/plywood_department/', plywood_department, name='plywood_department'),
    path('assign-misc-parts/', views.assign_misc_parts, name='assign_misc_parts'),
    path('add-to-misc-table/', views.add_to_misc_table, name='add_to_misc_table'),
    path('remove_from_misc/<int:part_id>/', views.remove_from_misc, name='remove_from_misc'),
    path('get_unassigned_parts/', views.get_unassigned_parts, name='your_view_for_unassigned_parts'),
    path('update-upholstery-assembly-status/', views.update_upholstery_assembly_status, name='update_upholstery_assembly_status'),
    path('management/update-upholstery-notes/<int:upholstery_id>/', views.update_upholstery_notes, name='update_upholstery_notes'),
    path('management/update-upholstery-comments/<int:upholstery_id>/', views.update_upholstery_comments, name='update_upholstery_comments'),
    path('import/', views.import_data, name='import_data'),
    path('import-csv/', views.import_csv, name='import_csv'),
    path('update_upholstery_comment2/<int:upholstery_id>/', views.update_upholstery_comment2, name='update_upholstery_comment2'),


 

    

    # Example: path('orders/', views.order_list, name='order_list'),
    # Add more URL patterns for other views in your app
]
