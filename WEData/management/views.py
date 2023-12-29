from django.shortcuts import render
from .models import Order
from django.db.models import Q

from django.db.models import Q



from django.core.paginator import Paginator
from .models import Order
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Order
from django.http import HttpResponse


def order_list(request):
    customer_query = request.GET.get('customer_search', '')
    order_query = request.GET.get('order_search', '')
    product_query = request.GET.get('product_search', '')
    job_query = request.GET.get('job_search', '')

    # Fetch orders based on the search criteria
    orders = Order.objects.all()
    if customer_query:
        orders = orders.filter(customer__name__icontains=customer_query)
    if order_query:
        orders = orders.filter(sage_order_number__icontains=order_query)
    if product_query:
        orders = orders.filter(part__product_code__icontains=product_query)
    if job_query:
        orders = orders.filter(job__icontains=job_query)

       # Pagination setup
    num_orders = int(request.GET.get('num_orders', 10))  # Default to 10 orders per page
    show_more = request.GET.get('show_more', False)
    if show_more:
        num_orders += 20  # Increase by x each time 'Show More' is clicked

    # Paginator setup
    paginator = Paginator(orders, num_orders)
    page_obj = paginator.get_page(1)  # Always show the first 'page'

    # Create a range for the template
    num_range = range(1, 6)  # Adjust the range as needed

    # Render the full page for non-AJAX requests
    return render(request, 'management/order_list.html', {
        'page_obj': page_obj,
        'customer_query': customer_query,
        'order_query': order_query,
        'product_query': product_query,
        'job_query': job_query,
        'num_orders': num_orders,
        'num_range': num_range
    })





from django.shortcuts import get_object_or_404
from .models import Customer, Order, PartDescription





def customer_orders(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)

    # Default sort order
    sort_order = request.GET.get('sort', '-order_date')

    # Determine the current sort field and direction
    current_sort_field = sort_order.lstrip('-')
    current_sort_direction = '-' if sort_order.startswith('-') else ''

    # Toggle sort direction if the same field is clicked again
    if 'sort' in request.GET and current_sort_field == request.GET['sort'].lstrip('-'):
        current_sort_direction = '' if current_sort_direction == '-' else '-'

    # Apply the sorting
    orders = Order.objects.filter(customer=customer).order_by(f'{current_sort_direction}{current_sort_field}')
    return render(request, 'management/customer_orders.html', {
        'customer': customer,
        'orders': orders,
        'current_sort_field': current_sort_field,
        'current_sort_direction': current_sort_direction
    })





from django.shortcuts import get_object_or_404
from .models import Order, Part, OrdertoJobBridge

def order_detail(request, sage_order_number):
    order = get_object_or_404(Order, sage_order_number=sage_order_number)
    parts = Part.objects.filter(sage_order_number=sage_order_number).select_related('product_code')

    # Fetch related job information for each part
    parts_with_jobs = [
        {
            'part': part,
            'job': OrdertoJobBridge.objects.filter(part_id=part.part_id).first(),  # Adjust field name as per your model
        }
        for part in parts
    ]

    return render(request, 'management/order_detail.html', {
        'order': order,
        'parts_with_jobs': parts_with_jobs
    })




from django.http import JsonResponse
from .models import Order, Customer
from django.db.models import Q

def api_orders(request):
    status_filter = request.GET.get('status', 'all')
    orders_query = Order.objects.select_related('customer')

    if status_filter != 'all':
        # Assuming you have a 'status' field in your Order model
        orders_query = orders_query.filter(status=status_filter)

    orders = [
        {
            'sageOrderNumber': order.sage_order_number,
            'customerName': order.customer.name,
            'orderDate': order.order_date,
            'deliveryPostcode': order.delivery_postcode,
            'value': order.value,
            'orderNotes': order.order_notes
        }
        for order in orders_query
    ]

    return JsonResponse(orders, safe=False)





from django.shortcuts import render, get_object_or_404
from .models import OrdertoJobBridge, PickingProcess, CNCMachine, Workshop

def job_detail(request, job_id):
    job_bridges = OrdertoJobBridge.objects.filter(job=job_id)
    picking_infos = PickingProcess.objects.filter(job=job_id)
    cnc_infos = CNCMachine.objects.filter(job=job_id)
    workshop_infos = Workshop.objects.filter(job=job_id)

    return render(request, 'management/job_detail.html', {
        'job_bridges': job_bridges,
        'picking_infos': picking_infos,
        'cnc_infos': cnc_infos,
        'workshop_infos': workshop_infos
    })
