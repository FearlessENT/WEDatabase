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






def is_picking(user):
    if user.groups.filter(name='Picking').exists() or is_admin(user):
        return True
    else:
        return False



def is_cncmachining(user):
    if user.groups.filter(name='CNCMachining').exists() or is_admin(user):
        return True
    else:
        return False



def is_orders(user):
    if user.groups.filter(name='Orders').exists() or is_admin(user):
        return True
    else:
        return False


def is_job(user):
    if user.groups.filter(name='Jobs').exists() or is_admin(user):
        return True
    else:
        return False
    


def is_assembly(user):
    if user.groups.filter(name='Assembly').exists() or is_admin(user):
        return True
    else:
        return False




def is_upholstery(user):
    if user.groups.filter(name='Upholstery').exists() or is_admin(user):
        return True
    else:
        return False




def is_minikitchen(user):
    if user.groups.filter(name='MiniKitchen').exists() or is_admin(user):
        return True
    else:
        return False
    


def is_plywood(user):
    if user.groups.filter(name='Plywood').exists() or is_admin(user):
        return True
    else:
        return False


def is_misc(user):
    if user.groups.filter(name='Misc').exists() or is_admin(user):
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
@user_passes_test(is_orders)
def order_list(request):
    # Existing search queries
    customer_query = request.GET.get('customer_search', '')
    order_query = request.GET.get('order_search', '')
    product_query = request.GET.get('product_search', '')
    job_query = request.GET.get('job_search', '')
    status_filter = request.GET.get('status_filter', 'all')  # New status filter

    sort_order = request.GET.get('sort_order', 'newest')  # Default to 'newest'

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



    if sort_order == 'newest':
        orders = orders.order_by('sage_order_number')  # Assumes 'id' is the primary key
    elif sort_order == 'oldest':
        orders = orders.order_by('-sage_order_number')


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
        'status_filter': status_filter,
        'sort_order': sort_order
    })




from django.shortcuts import get_object_or_404
from .models import Customer, Order, PartDescription






from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from .models import Customer, Order

@login_required
@user_passes_test(is_orders)
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
@user_passes_test(is_orders)
def order_detail(request, sage_order_number):
    order = get_object_or_404(Order, sage_order_number=sage_order_number)
    parts = Part.objects.filter(sage_order_number=sage_order_number).select_related('product_code', 'job')

    # Use the 'user_notes' field to extract the codes
    if order.order_notes:
        print(order.order_notes)
        codes_list = [code.strip() for code in order.order_notes.split(';') if code.strip()]
        codes = [{'label': c.split(';')[0].strip(), 'value': c.split(':')[1].strip()} for c in codes_list if ':' in c]
    else:
        codes = []

    cleaned_order_value = clean_value(order.value)

    return render(request, 'management/order_detail.html', {
        'order': order,
        'parts': parts,
        'codes': codes
    })





from django.http import JsonResponse
from .models import Order, Customer
from django.db.models import Q

@login_required
@user_passes_test(is_orders)
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
@user_passes_test(is_job)
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

        # Update machine notes
        cnc_machines = CNCMachine.objects.filter(job_id=job_id)
        for machine in cnc_machines:
            machine_notes = request.POST.get(f'machine_notes_{machine.cnc_machine_id}', None)
            if machine_notes is not None:
                machine.notes = machine_notes
                machine.save()
                
        return redirect('job_detail', job_id=job.job_id)

    # Fetch parts linked to the job
    parts = Part.objects.filter(job=job)

    # Fetch orders linked to those parts
    orders = Order.objects.filter(part__job=job).distinct()

    # Fetch picking info linked to the job
    picking_infos = PickingProcess.objects.filter(job_id=job_id)

    # Fetch CNC machine info linked to the job
    cnc_infos = CNCMachine.objects.filter(job_id=job_id).values('cnc_machine_id', 'machine__machine_name', 'notes')
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
@user_passes_test(is_job)
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
@user_passes_test(is_job)
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
@user_passes_test(is_job)
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
@user_passes_test(is_job)
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
@user_passes_test(is_job)
def create_job(request):
    if request.method == 'POST':
        form = CreateJobForm(request.POST)
        if form.is_valid():
            new_job = form.save()

            cnc_machine_description = form.cleaned_data.get('CNCMachine')
            if cnc_machine_description:
                new_job.CNCMachine = cnc_machine_description
                new_job.save()

                # Create a new CNCMachine entry for this job
                CNCMachine.objects.create(
                    machine=cnc_machine_description,
                    job=new_job
                )

            # Assign parts to the new job only if selected
            selected_parts = request.session.get('selected_parts', [])
            if selected_parts:
                Part.objects.filter(part_id__in=selected_parts).update(job=new_job)

            # Clear the temporary storage
            request.session.pop('selected_parts', None)

            return redirect('job_list')
    else:
        form = CreateJobForm()

    # Exclude parts that are in MiscTable from the unassigned parts list
    misc_part_ids = MiscTable.objects.values_list('part__part_id', flat=True)
    unassigned_parts = Part.objects.filter(job__isnull=True).exclude(part_id__in=misc_part_ids).select_related(
        'sage_order_number', 
        'sage_order_number__customer', 
        'product_code'
    )

    return render(request, 'management/create_job.html', {
        'form': form,
        'unassigned_parts': unassigned_parts,
    })






    
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
@user_passes_test(is_job)
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
@user_passes_test(is_job)
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
@user_passes_test(is_job)
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
@user_passes_test(is_job)
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
from .models import CNCMachine, Job
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Sum, Case, When, IntegerField, Q, Value
from django.db.models.functions import Cast

@login_required
@user_passes_test(is_cncmachining)
def cnc_operator_jobs(request):
    machined_status = request.GET.get('machined_status', 'all')
    selected_machine_id = request.GET.get('machine', '')
    # Attempt to get 'num_machines' from the session if not present in the GET request
    num_machines = request.GET.get('num_machines') or request.session.get('num_machines', 20)

    try:
        num_machines = int(request.GET.get('num_machines', 10))
    except ValueError:
        num_machines = 10

    machines_query = CNCMachine.objects.filter(machine_id=selected_machine_id).order_by('-cnc_machine_id') if selected_machine_id else CNCMachine.objects.all().order_by('-cnc_machine_id')
    all_cnc_machines = CNCMachineDescription.objects.all().order_by('-pk')

    if selected_machine_id:
        machines_query = machines_query.filter(machine__machine_id=selected_machine_id)

    if machined_status == 'machined':
        machines_query = machines_query.filter(machine_stage='Machined')
    elif machined_status == 'not_machined':
        machines_query = machines_query.exclude(machine_stage='Machined')

    paginator = Paginator(machines_query, num_machines)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Filter jobs based on the selected CNC machine
    jobs_query = Job.objects.filter(cncmachine__in=machines_query)

    # Calculate totals independently of the machined_status filter
    totals = Job.objects.filter(cncmachine__in=machines_query).annotate(
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
        'num_machines': num_machines,
        'machined_status': machined_status,
        'all_cnc_machines': all_cnc_machines,
        'selected_machine_id': selected_machine_id,
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
@user_passes_test(is_cncmachining)
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
@login_required
@user_passes_test(is_cncmachining)
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
@login_required
@user_passes_test(is_cncmachining)
def update_job_mm8_stage(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        job_id = data.get('job_id')
        mm8_stage = data.get('mm8_machine_stage')

        job = get_object_or_404(Job, job_id=job_id)
        job.mm8_status = mm8_stage  
        if mm8_stage == 'Machined' and job.mm18_status == 'Machined':
            job.machined_by = request.user

        job.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)






from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@login_required
@user_passes_test(is_cncmachining)
def update_job_mm18_stage(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        job_id = data.get('job_id')
        mm18_stage = data.get('mm18_machine_stage')

        job = get_object_or_404(Job, job_id=job_id)
        job.mm18_status = mm18_stage 
        if mm18_stage == 'Machined' and job.mm8_status == 'Machined':
            job.machined_by = request.user
        job.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)










from django.shortcuts import render
from .models import PickingProcess

from .models import Job, Part

from django.core.paginator import Paginator
from django.db.models import Prefetch

@login_required
@user_passes_test(is_picking)
def picking_department(request):
    picking_status_filter = request.GET.get('picking_status', None)

    # Fetch jobs where either mm8_status or mm18_status is 'Machined'
    jobs_with_picking = Job.objects.select_related('CNCMachine').filter(
        Q(mm8_status='Machined') | Q(mm18_status='Machined')
    )

    # Apply picking status filter if provided
    if picking_status_filter:
        if picking_status_filter in ['Picked', 'On Hold', 'Waiting']:
            jobs_with_picking = jobs_with_picking.filter(
                pickingprocess__picking_status=picking_status_filter
            )
        elif picking_status_filter == 'not_picked':
            jobs_with_picking = jobs_with_picking.exclude(
                pickingprocess__picking_status='Picked'
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
@login_required
@user_passes_test(is_picking)
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
@login_required
@user_passes_test(is_picking)
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
@login_required
@user_passes_test(is_picking)
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
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Workshop, WorkshopTypes



@login_required
@user_passes_test(is_assembly)
def assembly_department(request):
    assembly_status_filter = request.GET.get('assembly_status', 'all')
    picking_status_filter = request.GET.get('picking_status', 'all')
    sort_order = request.GET.get('sort_order', 'newest')  # Default to 'newest'
    search_query = request.GET.get('search', '')

    if 'clear' in request.GET:
        search_query = ''

    workshops_query = Workshop.objects.filter(workshop_id__workshop_name="assembly")

    if search_query:
        print("search enabled ", search_query)
        workshops_query = workshops_query.filter(
            Q(sage_order_number__delivery_postcode__icontains=search_query) |
            Q(sage_order_number__sage_order_number__icontains=search_query) |
            Q(product_code__product_code__icontains=search_query) |
            Q(product_code__product_description__icontains=search_query)
        )


    if sort_order == 'newest':
        workshops_query = workshops_query.order_by('-id')
    elif sort_order == 'oldest':
        workshops_query = workshops_query.order_by('id')

    if assembly_status_filter in ['Built', 'Waiting']:
        workshops_query = workshops_query.filter(assembly_status=assembly_status_filter)

    if picking_status_filter == 'not_waiting':
        orders_with_non_waiting_parts = Order.objects.exclude(part__picking_status='Waiting').values_list('sage_order_number', flat=True)
        workshops_query = workshops_query.filter(sage_order_number__in=orders_with_non_waiting_parts)

    num_items = int(request.GET.get('num_items', 20))
    if 'show_more' in request.GET:
        num_items += 20

    paginator = Paginator(workshops_query.distinct(), num_items)
    page_obj = paginator.get_page(1)
    
    return render(request, 'assembly/assembly_department.html', {
        'page_obj': page_obj,
        'assembly_status_filter': assembly_status_filter,
        'picking_status_filter': picking_status_filter,
        'sort_order': sort_order,
        'search_query': search_query,
    })








from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Workshop
import json
from django.utils import timezone

@csrf_exempt
@login_required
@user_passes_test(is_assembly)
def update_assembly_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        workshop_id = data.get('workshop_id')
        assembly_status = data.get('assembly_status')

        workshop = get_object_or_404(Workshop, id=workshop_id)
        workshop.assembly_status = assembly_status
        workshop.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)





from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Workshop

@login_required
@user_passes_test(is_assembly)  # Adapt this decorator to your assembly permission logic
def update_workshop_notes(request, workshop_id):
    if request.method == 'POST':
        workshop_notes = request.POST.get('workshop_notes')

        workshop = get_object_or_404(Workshop, id=workshop_id)
        workshop.notes = workshop_notes
        workshop.save()

        # Redirect back to the referring page
        referer_url = request.META.get('HTTP_REFERER')
        if referer_url:
            return HttpResponseRedirect(referer_url)
        else:
            # Fallback redirect if referer URL is not available
            return redirect('assembly_department')  # Replace with your actual default redirect URL

    # Handle non-POST requests here
    # ...

    # Optional: Redirect or show an error for non-POST requests
    return redirect('assembly_department')





























from django.http import HttpResponseRedirect
from .models import Part

def update_assembly_comments(request):
    if request.method == 'POST':
        part_id = request.POST.get('part_id')
        comment1 = request.POST.get('comment1', '')
        comment2 = request.POST.get('comment2', '')
        
        # Fetch the part object and update the comments
        try:
            part = Part.objects.get(id=part_id)
            part.comment1 = comment1
            part.comment2 = comment2
            part.save()
            # Redirect to a success page or back to the assembly department page
            return HttpResponseRedirect('/management/assembly/assembly_department/')
        except Part.DoesNotExist:
            # Handle the error or redirect to an error page
            pass

    # If not POST or part does not exist, redirect to a default page
    return HttpResponseRedirect('/management/assembly/assembly_department/')



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Workshop
import json

@csrf_exempt
@login_required
@user_passes_test(is_assembly)
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














@login_required
@user_passes_test(is_minikitchen)
def minikitchen_department(request):
    assembly_status_filter = request.GET.get('assembly_status', 'all')
    sort_order = request.GET.get('sort_order', 'newest')  # Default to 'newest'
    search_query = request.GET.get('search', '')  # Retrieve the search query

    if 'clear' in request.GET:
        search_query = ''
    
    workshop_type = WorkshopTypes.objects.get(workshop_name="Minikitchen")
    workshops_query = Workshop.objects.filter(workshop_id=workshop_type)

    if search_query:
        workshops_query = workshops_query.filter(
            Q(sage_order_number__delivery_postcode__icontains=search_query) |
            Q(sage_order_number__sage_order_number__icontains=search_query) |
            Q(product_code__product_code__icontains=search_query) |
            Q(product_code__product_description__icontains=search_query)
        )

    if assembly_status_filter in ['Built', 'Waiting']:
        workshops_query = workshops_query.filter(assembly_status=assembly_status_filter)

    if sort_order == 'newest':
        workshops_query = workshops_query.order_by('-id')
    elif sort_order == 'oldest':
        workshops_query = workshops_query.order_by('id')

    num_items = int(request.GET.get('num_items', 20))
    if 'show_more' in request.GET:
        num_items += 20

    paginator = Paginator(workshops_query, num_items)
    page_obj = paginator.get_page(1)
    
    return render(request, 'assembly/minikitchen_department.html', {
        'page_obj': page_obj,
        'assembly_status_filter': assembly_status_filter,
        'sort_order': sort_order,
        'search_query': search_query,
    })












from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Workshop, WorkshopTypes
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(is_plywood)  # Ensure you have an appropriate permission-checking decorator
def plywood_department(request):
    assembly_status_filter = request.GET.get('assembly_status', 'all')
    sort_order = request.GET.get('sort_order', 'newest')  # Default to 'newest'
    search_query = request.GET.get('search', '')  # Retrieve the search query

    if 'clear' in request.GET:
        search_query = ''
    
    workshop_type = WorkshopTypes.objects.get(workshop_name="Plywood")
    workshops_query = Workshop.objects.filter(workshop_id=workshop_type)

    # Filter based on search query if provided
    if search_query:
        workshops_query = workshops_query.filter(
            Q(sage_order_number__delivery_postcode__icontains=search_query) |
            Q(sage_order_number__sage_order_number__icontains=search_query) |
            Q(product_code__product_code__icontains=search_query) |
            Q(product_code__product_description__icontains=search_query)
        )

    # Apply filters for assembly status
    if assembly_status_filter in ['Built', 'Waiting']:
        workshops_query = workshops_query.filter(assembly_status=assembly_status_filter)

    # Sorting
    if sort_order == 'newest':
        workshops_query = workshops_query.order_by('-id')
    elif sort_order == 'oldest':
        workshops_query = workshops_query.order_by('id')

    # Pagination
    num_items = int(request.GET.get('num_items', 20))
    if 'show_more' in request.GET:
        num_items += 20

    paginator = Paginator(workshops_query.distinct(), num_items)
    page_obj = paginator.get_page(1)
    
    return render(request, 'assembly/plywood_department.html', {
        'page_obj': page_obj,
        'assembly_status_filter': assembly_status_filter,
        'sort_order': sort_order,
        'search_query': search_query,
    })
























from django.utils import timezone
from django.db.models import F, ExpressionWrapper, fields, DateField
from django.shortcuts import render
from .models import Upholstery

@login_required
@user_passes_test(is_upholstery)
def upholstery_department(request):
    assembly_status_filter = request.GET.get('assembly_status', 'all')
    search_query = request.GET.get('search', '')
    sort_order = request.GET.get('sort_order', 'newest')
    num_items = int(request.GET.get('num_items', 20))

    if 'show_more' in request.GET:
        num_items += 20  # Increment the items

   
    upholsteries_query = Upholstery.objects.select_related('part__sage_order_number').annotate(
        days_old=ExpressionWrapper(
            timezone.now().date() - F('part__sage_order_number__order_date'),
            output_field=fields.DurationField()
        )
    )
    
    
    if assembly_status_filter != 'all':
        upholsteries_query = upholsteries_query.filter(assembly_status=assembly_status_filter)

    if search_query:
        upholsteries_query = upholsteries_query.filter(
            Q(part__product_code__icontains=search_query) |
            Q(part__sage_order_number__icontains=search_query)
            # Add other search filters as necessary
        )

    if sort_order == 'newest':
        upholsteries_query = upholsteries_query.order_by('-part__part_id')
    elif sort_order == 'oldest':
        upholsteries_query = upholsteries_query.order_by('part__part_id')


    
    paginator = Paginator(upholsteries_query, num_items)  # Use the updated num_items
    page_obj = paginator.get_page(1)  # Always return the first page but with more items

    


    context = {
        'page_obj': page_obj,
        'assembly_status_filter': assembly_status_filter,
        'search_query': search_query,
        'sort_order': sort_order,
        'num_items': num_items,  # Pass the updated num_items back to the template
    }

    return render(request, 'upholstery/upholstery_department.html', context)






















from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import MiscTable, Part  # Make sure to import the Part model as well


@login_required
@user_passes_test(is_misc)
def assign_misc_parts(request):
    # Fetch only the 5 most recent misc entries, sorted by date_added
    misc_entries = MiscTable.objects.all()[:5]
    misc_part_ids = MiscTable.objects.values_list('part__part_id', flat=True)
    unassigned_parts = Part.objects.filter(job__isnull=True).exclude(part_id__in=misc_part_ids)

    # Pagination logic
    num_items = int(request.GET.get('num_items', 20))
    if 'show_more' in request.GET:
        num_items += 20

    paginator = Paginator(unassigned_parts, num_items)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'management/assign_misc_parts.html', {
        'misc_entries': misc_entries,
        'page_obj': page_obj,
        'num_items': num_items
    })






from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Part, MiscTable  # Adjust the import path as necessary

@csrf_exempt
@require_POST
@login_required
@user_passes_test(is_misc)
def add_to_misc_table(request):
    try:
        data = json.loads(request.body)
        part_id = data.get('partId')
        part = Part.objects.get(pk=part_id)
        MiscTable.objects.create(part=part)
        
        # Since the page will refresh, no need to send back part details
        return JsonResponse({'success': True})
    except Part.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Part does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MiscTable

@csrf_exempt
def remove_from_misc(request, part_id):
    try:
        misc_entry = MiscTable.objects.get(part__part_id=part_id)
        misc_entry.delete()
        return JsonResponse({'success': True})
    except MiscTable.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)




from django.http import JsonResponse
from django.core import serializers

@login_required
def get_unassigned_parts(request):
    misc_part_ids = MiscTable.objects.values_list('part__part_id', flat=True)
    unassigned_parts = Part.objects.filter(job__isnull=True).exclude(part_id__in=misc_part_ids)
    # Serialize the queryset to JSON
    unassigned_parts_json = serializers.serialize('json', unassigned_parts)
    return JsonResponse({'unassignedParts': unassigned_parts_json})

















from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Upholstery
import json

@csrf_exempt
@login_required
@user_passes_test(is_upholstery)
def update_upholstery_assembly_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        upholstery_id = data.get('upholstery_id')  # Make sure this matches the data sent from the frontend
        assembly_status = data.get('assembly_status')

        # Use the correct field name to lookup the Upholstery object
        upholstery = get_object_or_404(Upholstery, upholstery_id=upholstery_id)
        upholstery.assembly_status = assembly_status
        upholstery.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)









@login_required
# Adapt this decorator to your upholstery permission logic
def update_upholstery_notes(request, upholstery_id):
    if request.method == 'POST':
        assembly_notes = request.POST.get('assembly_notes')

        upholstery = get_object_or_404(Upholstery, upholstery_id=upholstery_id)
        upholstery.assembly_notes = assembly_notes
        upholstery.save()

        # Redirect back to the referring page
        referer_url = request.META.get('HTTP_REFERER')
        if referer_url:
            return HttpResponseRedirect(referer_url)
        else:
            # Fallback redirect if referer URL is not available
            return redirect('upholstery_department')  # Adjust to your actual default redirect URL

    # Optional: Redirect or show an error for non-POST requests
    return redirect('upholstery_department')






from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Upholstery

@login_required
@user_passes_test(is_upholstery)  # Adapt this to your upholstery permission logic
def update_upholstery_comments(request, upholstery_id):
    if request.method == 'POST':
        upholstery_comments = request.POST.get('upholstery_comments')

        upholstery = get_object_or_404(Upholstery, upholstery_id=upholstery_id)
        upholstery.comments = upholstery_comments
        upholstery.save()

        # Redirect back to the referring page
        referer_url = request.META.get('HTTP_REFERER')
        if referer_url:
            return HttpResponseRedirect(referer_url)
        else:
            # Fallback redirect if referer URL is not available
            return redirect('upholstery_department')  # Adjust to your actual default redirect URL

    # Optional: Handle non-POST requests or show an error
    return redirect('upholstery_department')




from django.shortcuts import render
from django.http import HttpResponse
import csv

def import_data(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']
        # Assuming you have a model called 'MyModel' to which you want to import CSV data
        reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
        for row in reader:
            # Process the CSV rows and save to your model
            pass  # Replace with your logic
        return HttpResponse('Data imported successfully')
    return render(request, 'import/Import.html')



def convert_date_format(date):
  # check if the date is empty
  if not date:
    # return None
    return None
  # split the date by "/"
  day, month, year = date.split("/")
  # join the year, month, and day by "-"
  new_date = "-".join([year, month, day])
  # return the new date
  return new_date



from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import transaction

def import_csv(request):
    if request.method == 'POST' and 'file' in request.FILES:
        csv_file = request.FILES['file']
        # Process your CSV file here
        csvfile = csv_file.read().decode('utf-8').splitlines()






        # Temporary storage for customers and orders for console printing
        temp_customers = {}
        temp_orders = {}
        order_values = {}

    
        reader = csv.DictReader(csvfile)
        # Validate that 'Dept' is a column in the CSV. If not, print an error message.
        if 'Dept ' not in reader.fieldnames:
            raise ValueError("CSV file does not contain 'Dept' column or the column header is misspelled.")

        
        with transaction.atomic():
            for row in reader:

                


                customer_name = row['Customer']
                sage_order_number = row['Sales Order']
                dept = row['Dept ']
                
                if dept != 'Default':
                    # Convert the 'Unit Price' to float and accumulate the total value per order
                    unit_price_str = row.get('Unit Price', '0').strip()
                    unit_price = 0.0  # Default value if 'Unit Price' is empty
                    if unit_price_str:
                        try:
                            unit_price = float(unit_price_str)
                        except ValueError:
                            # Log the error or handle it as per your application's requirements
                            print(f"Could not convert {unit_price_str} to float for order {row['Sales Order']}. Defaulting to 0.")
                    order_values[sage_order_number] = order_values.get(sage_order_number, 0) + unit_price
                
                # Check if customer exists, if not create a new one
                customer, created = Customer.objects.get_or_create(
                    name=customer_name
                )
                # Add to temp_customers for console printing
                if created:
                    temp_customers[customer_name] = customer.customer_id
                
                # Now, handle the order
                order_date = row['Order Date']
                order_date = convert_date_format(order_date)
                delivery_postcode = row['Delivery Address']
                customer_postcode = row['Sales Order Address']
                order_taken_by = row['Order Taken By']
                estimated_delivery_wkc = row['Despatch By']
                estimated_delivery_wkc = convert_date_format(estimated_delivery_wkc)
                # ... Extract other fields as necessary

                total_value = order_values.get(sage_order_number, 0)
                # Check if order exists, if not create a new one
                order, created = Order.objects.update_or_create(
                    sage_order_number=sage_order_number,
                    defaults={
                        'customer': customer,
                        'order_date': order_date,
                        'delivery_postcode': delivery_postcode,
                        'customer_postcode': customer_postcode,
                        'order_taken_by': order_taken_by,
                        'estimated_delivery_wkc': estimated_delivery_wkc,
                        'value': total_value,  # Set the total value of parts for the order
                        # ... Set other fields as necessary
                    }
                )
                # Add to temp_orders for console printing
                if created:
                    temp_orders[order.sage_order_number] = {
                        'customer_id': customer.customer_id,
                        'order_date': order.order_date,
                        'value': total_value,  # Use the accumulated total value
                        # ... Include other fields as necessary
                    }


            # transaction.set_rollback(True)

                        
        # Print temporary tables to the console
        print("Temporary Customers Table")
        for name, id in temp_customers.items():
            print(f"Customer Name: {name}, Customer ID: {id}")

        print("\nTemporary Orders Table")
        for order_num, order_data in temp_orders.items():
            print(f"Order Number: {order_num}, Order Data: {order_data}")

            







        # Redirect or respond after processing
        return redirect('import_data') 
    return HttpResponse('Failed to upload file', status=400)
