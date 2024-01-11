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






def clean_value(value):
    # Remove non-numeric characters except for the decimal point
    cleaned_value = ''.join(c for c in value if c.isdigit() or c == '.')
    try:
        return float(cleaned_value)
    except ValueError:
        return 0






















def order_list(request):
    # Existing search queries
    customer_query = request.GET.get('customer_search', '')
    order_query = request.GET.get('order_search', '')
    product_query = request.GET.get('product_search', '')
    job_query = request.GET.get('job_search', '')
    status_filter = request.GET.get('status_filter', 'all')  # New status filter

    # Fetch orders based on the search criteria
    orders = Order.objects.all()
    if customer_query:
        orders = orders.filter(customer__name__icontains=customer_query)
    if order_query:
        orders = orders.filter(sage_order_number__icontains=order_query)
    if product_query:
        orders = orders.filter(part__product_code__icontains=product_query)
    if job_query:
        orders = Order.objects.filter(part__job__job_name__icontains=job_query).distinct()

    # Apply status filter
    if status_filter == 'complete':
        orders = orders.filter(status='Complete')  # Adjust field and value as per your model
    elif status_filter == 'incomplete':
        orders = orders.exclude(status='Complete')  # Adjust field and value as per your model

    # Pagination setup
    num_orders = int(request.GET.get('num_orders', 20))  # Default to 10 orders per page
    show_more = request.GET.get('show_more', False)
    if show_more:
        num_orders += 20

    paginator = Paginator(orders, num_orders)
    page_obj = paginator.get_page(1)

    # Create a range for the template
    num_range = range(1, 6)

    return render(request, 'management/order_list.html', {
        'page_obj': page_obj,
        'customer_query': customer_query,
        'order_query': order_query,
        'product_query': product_query,
        'job_query': job_query,
        'num_orders': num_orders,
        'num_range': num_range,
        'status_filter': status_filter  # Pass the status filter to the template
    })




from django.shortcuts import get_object_or_404
from .models import Customer, Order, PartDescription






from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from .models import Customer, Order

def customer_orders(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)

    # Retrieve filter and search parameters from the request
    order_query = request.GET.get('order_search', '')
    product_query = request.GET.get('product_search', '')
    status_filter = request.GET.get('status_filter', 'all')
    num_orders = int(request.GET.get('num_orders', 20))  # Default to 20 orders per page
    show_more = request.GET.get('show_more', False)

    if show_more:
        num_orders += 20  # Increase by 20 each time 'Show More' is clicked

    # Fetch orders based on the search criteria and customer ID
    orders = Order.objects.filter(customer=customer)

    if order_query:
        orders = orders.filter(sage_order_number__icontains=order_query)
    if product_query:
        orders = orders.filter(part__product_code__icontains=product_query)
    if status_filter == 'complete':
        orders = orders.filter(status='Complete')
    elif status_filter == 'incomplete':
        orders = orders.exclude(status='Complete')


    # Clean and aggregate the total value of all orders
    total_value = round(sum(clean_value(order.value) for order in orders), 2)
    

    # Pagination setup
    paginator = Paginator(orders, num_orders)
    page_obj = paginator.get_page(1)

    # Create a range for the template
    num_range = range(1, 6)

    return render(request, 'management/customer_orders.html', {
        'customer': customer,
        'page_obj': page_obj,
        'order_query': order_query,
        'product_query': product_query,
        'status_filter': status_filter,
        'num_orders': num_orders,
        'total_value': total_value,
        'num_range': num_range
    })















from django.shortcuts import render, get_object_or_404
from .models import Order, Part, Job

def order_detail(request, sage_order_number):
    order = get_object_or_404(Order, sage_order_number=sage_order_number)
    parts = Part.objects.filter(sage_order_number=sage_order_number).select_related('product_code', 'job')

    # No need to fetch job information separately as it's already joined with parts
    cleaned_order_value = clean_value(order.value)

    return render(request, 'management/order_detail.html', {
        'order': order,
        'parts': parts
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
from .models import Job, Part, Order, PickingProcess, CNCMachine, Workshop

def job_detail(request, job_id):
    # Ensure that job_id is correctly used to query the Job model
    job = get_object_or_404(Job, job_id=job_id)

    # Fetch parts linked to the job
    parts = Part.objects.filter(job=job)

    # Fetch orders linked to those parts
    orders = Order.objects.filter(part__job=job).distinct()

    # Fetch picking info linked to the job
    picking_infos = PickingProcess.objects.filter(job_id=job_id)

    # Fetch CNC machine info linked to the job
    cnc_infos = CNCMachine.objects.filter(job_id=job_id)
    # Fetch CNC machine information for each part
    cnc_status = CNCMachine.objects.filter(job=job).first()
    machining_status = cnc_status.machine_stage if cnc_status else 'Not Available'



    # Fetch workshop info linked to the job
    workshop_infos = Workshop.objects.filter(sage_order_number__part__job_id=job_id).distinct()


    return render(request, 'management/job_detail.html', {
        'job': job,
        'parts': parts,
        'orders': orders,
        'picking_infos': picking_infos,
        'cnc_infos': cnc_infos,
        'machining_status': machining_status,
        'workshop_infos': workshop_infos
    })








from django.shortcuts import redirect


def update_order_notes(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        user_notes = request.POST.get('user_notes')

        order = Order.objects.get(sage_order_number=order_id)
        order.user_notes = user_notes
        order.save()

        return redirect('order_list')  # Redirect back to the order list page








# from .models import Job

# def job_search(request):
#     job_query = request.GET.get('job_query', '')

#     # Fetch jobs based on the search query
#     jobs = Job.objects.filter(job_number__icontains=job_query)

#     # Additional logic to fetch related data

#     return render(request, 'management/job_search.html', {
#         'jobs': jobs,
#         'job_query': job_query
#     })





from django.shortcuts import render
from .models import Order, Part, OrdertoJobBridge

def job_search_results(request):
    job_query = request.GET.get('job_search', '')

    if job_query:
        orders = Order.objects.filter(part__job__job_name__icontains=job_query).distinct()
    else:
        orders = Order.objects.none()

    return render(request, 'management/job_search_results.html', {
        'orders': orders,
        'job_query': job_query
    })




from django.shortcuts import render
from .models import Job, Part
from django.core.paginator import Paginator
from django.db.models import Max, Q

def job_list(request):
    job_query = request.GET.get('job_search', '')

    # Fetch jobs along with the newest order date for each job
    jobs = Job.objects.annotate(
        newest_order_date=Max('part__sage_order_number__order_date')
    )

    # Apply job name search filter if provided
    if job_query:
        jobs = jobs.filter(job_name__icontains=job_query)

    jobs = jobs.order_by('-newest_order_date')

    num_jobs = int(request.GET.get('num_jobs', 30))  # Default to 10 jobs per page
    show_more = request.GET.get('show_more', False)

    if show_more:
        num_jobs += 20  # Increase by 10 each time 'Show More' is clicked

    # Pagination setup
    paginator = Paginator(jobs, num_jobs)
    page_obj = paginator.get_page(1)

    return render(request, 'management/job_list.html', {
        'page_obj': page_obj,
        'job_query': job_query  # Pass the job query to the template
    })





from django.shortcuts import get_object_or_404, redirect
from .models import Job

def update_job_notes(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(Job, job_id=job_id)
        job_notes = request.POST.get('job_notes')
        job.notes = job_notes
        job.save()

        return redirect('job_detail', job_id=job.job_id)  # Redirect back to the job detail page









from django.shortcuts import render, redirect
from .models import Job, Part
from .forms import CreateJobForm

def create_job(request):
    if request.method == 'POST':
        form = CreateJobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list')  # Redirect to the job list page after creation

    else:
        form = CreateJobForm()

    # Fetch parts not currently assigned to a job
    unassigned_parts = Part.objects.filter(job__isnull=True)

    return render(request, 'management/create_job.html', {
        'form': form,
        'unassigned_parts': unassigned_parts,
    })
