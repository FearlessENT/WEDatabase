from django.shortcuts import render
from .models import Order
from django.db.models import Q

from django.db.models import Q



from django.core.paginator import Paginator
from .models import Order




def order_list(request):
    customer_query = request.GET.get('customer_search', '')
    order_query = request.GET.get('order_search', '')
    product_query = request.GET.get('product_search', '')
    job_query = request.GET.get('job_search', '')

    orders = Order.objects.all()

    if customer_query:
        orders = orders.filter(customer__name__icontains=customer_query)
        # Add more customer-related filters here

    if order_query:
        orders = orders.filter(sage_order_number__icontains=order_query)

    if product_query:
        orders = orders.filter(part__product_code__icontains=product_query)

    if job_query:
        orders = orders.filter(job__icontains=job_query)



    # Convert num_orders to an integer
    num_orders = int(request.GET.get('num_orders', 10))  # Default to 10

    # Paginator setup
    paginator = Paginator(orders, num_orders)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'management/order_list.html', {
        'page_obj': page_obj,
        'customer_query': customer_query,
        'order_query': order_query,
        'product_query': product_query,
        'job_query': job_query,
        'num_orders': num_orders
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













def order_detail(request, sage_order_number):
    order = Order.objects.get(sage_order_number=sage_order_number)
    # Fetch additional related data as needed
    return render(request, 'management/order_detail.html', {'order': order})


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
