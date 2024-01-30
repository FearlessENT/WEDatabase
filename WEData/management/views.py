import json
from django.shortcuts import render
from .models import Order
from django.db.models import Q

from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test


from django.core.paginator import Paginator
from .models import Order
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Order
from django.http import HttpResponse









from django.contrib.auth.decorators import user_passes_test
def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def is_machinist(user):
    if user.groups.filter(name='Machinist').exists() or is_admin(user):
        return True
    else:
        return False




def is_reception(user):
    if user.groups.filter(name='Reception').exists() or is_admin(user):
        return True
    else:
        return False






def is_picking(user):
    if user.groups.filter(name='Picking').exists() or is_admin(user):
        return True
    else:
        return False









def clean_value(value):
    # Remove non-numeric characters except for the decimal point
    cleaned_value = ''.join(c for c in value if c.isdigit() or c == '.')
    try:
        return float(cleaned_value)
    except ValueError:
        return 0





















@login_required
@user_passes_test(is_reception)
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

@login_required
@user_passes_test(is_reception)
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

@login_required
@user_passes_test(is_reception)
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

@login_required
@user_passes_test(is_reception)
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


@login_required
@user_passes_test(is_reception)
def job_detail(request, job_id):
    job = get_object_or_404(Job, job_id=job_id)
    cnc_machines = CNCMachineDescription.objects.all()

    if request.method == 'POST':
        if 'cnc_machine_id' in request.POST:
            machine_id = request.POST.get('cnc_machine_id')
            if machine_id:
                job.CNCMachine_id = machine_id  # Update the machine ID
            else:
                job.CNCMachine = None  # Remove the machine assignment
        else:
            # Update job notes and additional fields
            job.job_notes = request.POST.get('job_notes')
            job.mm8_notes = request.POST.get('mm8_notes')
            job.mm8_quantity = request.POST.get('mm8_quantity')
            job.mm18_notes = request.POST.get('mm18_notes')
            job.mm18_quantity = request.POST.get('mm18_quantity')

        job.save()
        return redirect('job_detail', job_id=job.job_id)

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
        'workshop_infos': workshop_infos,
        'cnc_machines': cnc_machines
    })





from django.shortcuts import redirect

@login_required
@user_passes_test(is_reception)
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

@login_required
@user_passes_test(is_reception)
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
from .models import Job, Part, CNCMachineDescription
from django.core.paginator import Paginator
from django.db.models import Max

@login_required
@user_passes_test(is_reception)
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

    num_jobs = int(request.GET.get('num_jobs', 30))  # Default to 30 jobs per page
    show_more = request.GET.get('show_more', False)

    if show_more:
        num_jobs += 20  # Increase by 20 each time 'Show More' is clicked

    # Pagination setup
    paginator = Paginator(jobs, num_jobs)
    page_obj = paginator.get_page(1)

    # Fetch all CNC machines to populate the dropdowns
    cnc_machines = CNCMachineDescription.objects.all()

    return render(request, 'management/job_list.html', {
        'page_obj': page_obj,
        'job_query': job_query,
        'cnc_machines': cnc_machines  # Pass the CNC machines to the template
    })





from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Job

@login_required
@user_passes_test(is_reception)
def update_job_notes(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        job_notes = request.POST.get('job_notes')

        job = get_object_or_404(Job, job_id=job_id)
        job.job_notes = job_notes
        job.save()

        # Redirect back to the referring page
        referer_url = request.META.get('HTTP_REFERER')
        if referer_url:
            return HttpResponseRedirect(referer_url)
        else:
            # Fallback redirect if referer URL is not available
            return redirect('all_jobs')  # Replace 'all_jobs' with your default redirect URL

    # Handle non-POST requests here
    # ...





from django.shortcuts import render, redirect
from .forms import CreateJobForm
from .models import Job, Part

@login_required
@user_passes_test(is_reception)
def create_job(request):
    if request.method == 'POST':
        form = CreateJobForm(request.POST)
        if form.is_valid():
            new_job = form.save()

            # Assign the temporarily stored parts to this new job
            selected_parts = request.session.get('selected_parts', [])
            Part.objects.filter(part_id__in=selected_parts).update(job=new_job)


            # Clear the temporary storage
            del request.session['selected_parts']

            return redirect('job_list')
    else:
        form = CreateJobForm()

    






    
    unassigned_parts = Part.objects.filter(job__isnull=True).select_related(
        'sage_order_number', 
        'sage_order_number__customer', 
        'product_code'  
    )
    return render(request, 'management/create_job.html', {
    'form': form,
    'unassigned_parts': unassigned_parts,
    })






from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

@csrf_exempt
@require_POST
@login_required
@user_passes_test(is_reception)
def add_part_to_job(request):
    try:
        data = json.loads(request.body)
        part_id = data.get('part_id')

        # Store the part ID in the session
        if 'selected_parts' not in request.session:
            request.session['selected_parts'] = []
        if part_id not in request.session['selected_parts']:
            request.session['selected_parts'].append(part_id)
            request.session.modified = True  # To ensure the session is saved

        return JsonResponse({'status': 'success', 'message': 'Part added to job selection'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)




@csrf_exempt
@require_POST
@login_required
@user_passes_test(is_reception)
def remove_part_from_job(request):
    try:
        data = json.loads(request.body)
        part_id = data.get('part_id')

        # Remove the part ID from the session
        selected_parts = request.session.get('selected_parts', [])
        if part_id in selected_parts:
            selected_parts.remove(part_id)
            request.session['selected_parts'] = selected_parts
            request.session.modified = True

        return JsonResponse({'status': 'success', 'message': 'Part removed from job selection'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)







from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Job
import json

@csrf_exempt
@require_POST
@login_required
@user_passes_test(is_reception)
def update_job_machine(request):
    try:
        data = json.loads(request.body)
        job_id = data.get('job_id')
        machine_id = data.get('machine_id')


        job = Job.objects.get(pk=job_id)
        job.CNCMachine_id = machine_id
        job.save()

        return JsonResponse({'status': 'success', 'message': 'Job updated successfully'})

    except Job.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Job not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    


from django.shortcuts import get_object_or_404, redirect
from .models import Job, CNCMachineDescription

@login_required
@user_passes_test(is_reception)
def update_job_machine(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(Job, pk=job_id)
        machine_id = request.POST.get('cnc_machine_id')
        if machine_id:
            job.CNCMachine_id = machine_id  # Update the machine ID
        else:
            job.CNCMachine = None  # Remove the machine assignment
        job.save()

        return redirect('job_list')  # Redirect back to the job list















from django.db.models.functions import Cast
from django.db.models.fields import CharField
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import Part

def search_parts_ajax(request):
    if request.method == 'GET':
        search_term = request.GET.get('search_term', '')

        unassigned_parts = Part.objects.annotate(
            str_sage_order_number=Cast('sage_order_number', CharField())
        ).filter(
            job__isnull=True,
            str_sage_order_number__icontains=search_term
        ).select_related('sage_order_number', 'sage_order_number__customer', 'product_code')

        # Construct the JSON response manually
        parts_data = []
        for part in unassigned_parts:
            part_data = {
                'part_id': part.part_id,
                'product_code': part.product_code.product_code if part.product_code else 'N/A',  # Assuming 'product_code' is a field in PartDescription
                'product_description': part.product_code.product_description if part.product_code else 'N/A',
                'sage_order_number': part.sage_order_number.sage_order_number if part.sage_order_number else 'N/A',
                'customer_name': part.sage_order_number.customer.name if part.sage_order_number and part.sage_order_number.customer else 'N/A',
                'order_date': part.sage_order_number.order_date.strftime('%Y-%m-%d') if part.sage_order_number and part.sage_order_number.order_date else 'N/A',
                'estimated_delivery': part.sage_order_number.estimated_delivery_wkc.strftime('%Y-%m-%d') if part.sage_order_number and part.sage_order_number.estimated_delivery_wkc else 'N/A'
            }
            parts_data.append(part_data)

        return JsonResponse(parts_data, safe=False)















from django.shortcuts import render
from .models import CNCMachine
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Sum, Case, When, IntegerField
from django.db.models import Q
from django.db.models import Sum, Case, When, IntegerField, Q, Value, CharField
from django.db.models.functions import Cast, Coalesce


from .models import Job, Part

@login_required
@user_passes_test(is_machinist)
def cnc_operator_jobs(request):
    machine_name = None
    machined_status = request.GET.get('machined_status', 'all')  # New filter parameter

    try:
        num_machines = int(request.GET.get('num_machines', 10))
    except ValueError:
        num_machines = 10

    if hasattr(request.user, 'profile') and request.user.profile.assigned_cnc_machine:
        machine_id = request.user.profile.assigned_cnc_machine.machine_id
        machines_query = CNCMachine.objects.filter(machine__machine_id=machine_id)

        # Filter based on machined status
        if machined_status == 'machined':
            machines_query = machines_query.filter(machine_stage='Machined')  # Adjust the filter criteria as needed
        elif machined_status == 'not_machined':
            machines_query = machines_query.exclude(machine_stage='Machined')  # Adjust the filter criteria as needed

        if machines_query.exists():
            machine_name = machines_query.first().machine.machine_name

        paginator = Paginator(machines_query, num_machines)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    else:
        page_obj = None


    totals = Job.objects.annotate(
        converted_mm8_quantity=Case(
            When(mm8_quantity__iexact='none', then=Value(0)),
            default=Cast('mm8_quantity', IntegerField()),
            output_field=IntegerField()
        ),
        converted_mm18_quantity=Case(
            When(mm18_quantity__iexact='none', then=Value(0)),
            default=Cast('mm18_quantity', IntegerField()),
            output_field=IntegerField()
        )
    ).aggregate(
        total_mm8_quantity=Sum(
            Case(
                When(~Q(mm8_status='Machined'), then='converted_mm8_quantity'),
                default=0,
                output_field=IntegerField()
            )
        ),
        total_mm18_quantity=Sum(
            Case(
                When(~Q(mm18_status='Machined'), then='converted_mm18_quantity'),
                default=0,
                output_field=IntegerField()
            )
        )
    )
        

    return render(request, 'machining/cnc_operator_jobs.html', {
        'page_obj': page_obj,
        'machine_name': machine_name,
        'num_machines': num_machines,
        'machined_status': machined_status,  
        'total_mm8_quantity': totals['total_mm8_quantity'],
        'total_mm18_quantity': totals['total_mm18_quantity']
    })







from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.profile.user_role == 'machinist':  # Assuming 'user_role' attribute in user profile
            return '/cnc_operator_jobs'
        else:
            return '/default-page'






from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import CNCMachine

@login_required
def update_machine_notes(request):
    if request.method == 'POST':
        cnc_machine_id = request.POST.get('cnc_machine_id')
        machine_notes = request.POST.get('machine_notes')

        machine = get_object_or_404(CNCMachine, cnc_machine_id=cnc_machine_id)
        machine.notes = machine_notes
        machine.save()

        # Redirect back to the referring page
        referer_url = request.META.get('HTTP_REFERER')
        if referer_url:
            return HttpResponseRedirect(referer_url)
        else:
            # Fallback redirect if referer URL is not available
            return redirect('cnc_operator_jobs')  # Replace with your default redirect URL

    # Handle non-POST requests here
    # ...

    # Optional: Redirect or show an error for non-POST requests
    return redirect('cnc_operator_jobs')












import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import CNCMachine
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def update_machine_stage(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        machine_id = data.get('cnc_machine_id')
        machine_stage = data.get('machine_stage')

        logger.debug(f"Updating machine {machine_id} to stage {machine_stage}")  # Debugging

        machine = get_object_or_404(CNCMachine, cnc_machine_id=machine_id)
        machine.machine_stage = machine_stage

        if machine_stage == 'Machined':
            machine.date_complete = timezone.now()
            # Update the related job's machined_by field
            if machine.job:
                job = get_object_or_404(Job, job_id=machine.job.job_id)
                job.machined_by = request.user
                job.save()

        machine.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)







@csrf_exempt
def update_job_mm8_stage(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        job_id = data.get('job_id')
        mm8_stage = data.get('mm8_machine_stage')

        job = get_object_or_404(Job, job_id=job_id)
        job.mm8_status = mm8_stage  
        job.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)






from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def update_job_mm18_stage(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        job_id = data.get('job_id')
        mm18_stage = data.get('mm18_machine_stage')

        job = get_object_or_404(Job, job_id=job_id)
        job.mm18_status = mm18_stage 
        job.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)










from django.shortcuts import render
from .models import PickingProcess

from .models import Job, Part

from django.core.paginator import Paginator
from django.db.models import Prefetch

def picking_department(request):
    # Assuming CNCMachine has a field 'date_complete' and is related to Job
    jobs_with_picking = Job.objects.prefetch_related(
        Prefetch(
            'cncmachine_set',
            queryset=CNCMachine.objects.order_by('date_complete')
        ),
        'part_set'
    ).all()

    picking_status_filter = request.GET.get('picking_status', None)
    
    # Apply sorting by the date_complete of the related CNCMachine
    jobs_with_picking = jobs_with_picking.order_by('cncmachine__date_complete')

        # Apply filter if picking_status_filter is provided
    if picking_status_filter in ['Picked', 'On Hold', 'Waiting']:
        jobs_with_picking = jobs_with_picking.filter(
            pickingprocess__picking_status=picking_status_filter
        )


    # Pagination setup
    num_jobs = int(request.GET.get('num_jobs', 20))  # Default to 20 jobs per page
    show_more = request.GET.get('show_more', False)
    if show_more:
        num_jobs += 20

    paginator = Paginator(jobs_with_picking, num_jobs)
    page_obj = paginator.get_page(1)

    context = {'page_obj': page_obj, 'current_filter': picking_status_filter}
    return render(request, 'picking/picking_department.html', context)




@csrf_exempt
def update_picking_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        job_id = data.get('job_id')
        new_status = data.get('picking_status')

        # Assuming each job has one picking process
        picking_process = get_object_or_404(PickingProcess, job_id=job_id)
        picking_process.picking_status = new_status
        picking_process.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import PickingProcess
import json

@csrf_exempt
def save_picking_notes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        picking_id = data.get('picking_id')
        notes = data.get('notes')
        picking_status = data.get('picking_status')

        picking_process = get_object_or_404(PickingProcess, picking_id=picking_id)
        picking_process.notes = notes
        picking_process.picking_status = picking_status
        picking_process.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)





@csrf_exempt
def update_picking_notes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        job_id = data.get('job_id')
        notes = data.get('notes')

        picking_process = get_object_or_404(PickingProcess, job_id=job_id)
        picking_process.notes = notes
        picking_process.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)










from django.core.paginator import Paginator
from .models import Workshop, WorkshopTypes, Order, PartDescription

def assembly_department(request):



    workshop_filter = request.GET.get('workshop', None)
    workshops = Workshop.objects.select_related('workshop_id').all()

    if workshop_filter and workshop_filter.isdigit():
        workshops = workshops.filter(workshop_id__workshop_id=int(workshop_filter))

    workshop_types = WorkshopTypes.objects.all()
    num_processes = int(request.GET.get('num_processes', 20))







    # Fetch assembly processes with related data
    assembly_processes = Workshop.objects.select_related('workshop_id', 'sage_order_number', 'product_code').all()


    # Logic to calculate picking status for each part in the order
    for process in assembly_processes:
        # Example logic, adjust based on your actual model relations
        parts = Part.objects.filter(sage_order_number=process.sage_order_number)
        process.picking_status_indicator = all(part.picking_status == 'Picked' for part in parts)

    # Pagination setup
    num_processes = int(request.GET.get('num_processes', 20))
    paginator = Paginator(assembly_processes, num_processes)
    page_obj = paginator.get_page(1)

    context = {
        'page_obj': page_obj,
        'workshop_types': workshop_types,
        'current_filter': workshop_filter
    }
    return render(request, 'assembly/assembly_department.html', context)










from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Workshop
import json

@csrf_exempt
def update_assembly_notes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        job_id = data.get('job_id')
        notes = data.get('notes')

        workshop = get_object_or_404(Workshop, job_id=job_id)
        workshop.notes = notes
        workshop.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)













from django.core.paginator import Paginator
from .models import Workshop, WorkshopTypes, Order, PartDescription

def upholstery_department(request):


    return render(request, 'upholstery/upholstery_department.html')

