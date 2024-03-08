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



from django.db.models import F, Func, IntegerField
from django.db.models.functions import Now
from django.utils.timezone import now
class Days(Func):
    function = 'DATEDIFF'
    template = '%(function)s(%(expressions)s)'
    output_field = IntegerField()

    def __init__(self, expression, **extra):
        super().__init__(expression, Now(), **extra)

















@login_required
@user_passes_test(is_orders)
def order_list(request):
    # Existing search queries
    customer_query = request.GET.get('customer_search', '')
    order_query = request.GET.get('order_search', '')
    product_query = request.GET.get('product_search', '')
    job_query = request.GET.get('job_search', '')
    status_filter = request.GET.get('status_filter', 'all')  # New status filter
    custref_query = request.GET.get('custref_search', '')

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
        orders = orders.order_by('-sage_order_number')  # Assumes 'id' is the primary key
    elif sort_order == 'oldest':
        orders = orders.order_by('sage_order_number')


    if custref_query:
        # Filter orders by parsing order_notes for CUSTREF
        orders = [order for order in orders if 'CUSTREF: ' + custref_query in (order.order_notes or '')]


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
        'sort_order': sort_order,
        'custref_query': custref_query
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
from django.db.models import Prefetch
from .models import Order, Part, Job, PickingProcess, CNCMachine, Upholstery, Workshop, WorkshopTypes

from .models import Order, Part, Job, PickingProcess, Workshop, Upholstery, WorkshopTypes

@login_required
@user_passes_test(is_orders)
def order_detail2(request, sage_order_number):
    order = get_object_or_404(Order, sage_order_number=sage_order_number)
    parts = Part.objects.filter(sage_order_number=order).select_related('product_code', 'job')
    print(parts)

    workshops = {workshop.product_code_id: workshop for workshop in Workshop.objects.filter(sage_order_number=order)}
    upholsteries = {upholstery.part_id: upholstery for upholstery in Upholstery.objects.filter(part__sage_order_number=order)}

    # Prepare a dictionary to map job IDs to their associated picking statuses
    picking_statuses = PickingProcess.objects.filter(job__part__sage_order_number=order).values_list('job_id', 'picking_status')
    picking_status_map = {job_id: status for job_id, status in picking_statuses}

    # Annotate parts with assembly status and picking status
    for part in parts:
        # Handle assembly status as before
        if part.dept.lower() == 'upholstery':
            part.assembly_status = upholsteries.get(part.part_id, {}).get('assembly_status', 'N/A')
        else:
            workshop = workshops.get(part.product_code_id)
            part.assembly_status = workshop.assembly_status if workshop else 'N/A'

        # Annotate picking status
        part.picking_status = picking_status_map.get(part.job_id, 'N/A') if part.job else 'N/A'

    return render(request, 'management/order_detail.html', {
        'order': order,
        'parts': parts,
    })








from django.shortcuts import render, get_object_or_404
from .models import Order, Part, Upholstery

@login_required
@user_passes_test(is_orders)
def order_detail(request, sage_order_number):
    # Fetch the order using its sage order number
    order = get_object_or_404(Order, sage_order_number=sage_order_number)

    # Calculate days since the order date
    current_date = timezone.now().date()
    order_date = order.order_date
    days_old = (current_date - order_date).days

    # Fetch parts related to the order and use select_related for efficiency
    parts = Part.objects.filter(sage_order_number=order)
    # .select_related('product_code', 'job')

    codes = []
    if order.order_notes:
        notes = order.order_notes.split('; ')
        for note in notes:
            if ': ' in note:
                code, label = note.split(': ', 1)
                codes.append({'code': code, 'label': label})

    return render(request, 'management/order_detail.html', {
        'order': order,
        'parts': parts,
        'codes': codes,
        'days_old': days_old,  # Pass days_old to the template
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
    # Fetch workshop info linked to the job
    workshop_infos = Workshop.objects.filter(part__job=job).distinct()


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

    jobs = jobs.order_by('-job_id')

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
            with transaction.atomic():  # Ensures database integrity
                # Create the job with initial mm8 and mm18 statuses set to "Waiting"
                new_job = form.save(commit=False)  # Do not commit/save immediately to the database
                new_job.mm8_status = 'Waiting'
                new_job.mm18_status = 'Waiting'
                new_job.save()

                cnc_machine_description = form.cleaned_data.get('CNCMachine')
                if cnc_machine_description:
                    # Assuming the CNCMachine model is linked to the job and doesn't require immediate status updates
                    CNCMachine.objects.create(
                        machine=cnc_machine_description,
                        job=new_job
                    )

                # Assign parts to the new job only if selected
                selected_parts = request.session.get('selected_parts', [])
                if selected_parts:
                    Part.objects.filter(part_id__in=selected_parts).update(job=new_job)

                # Initialize picking process for the job with the default status "Waiting"
                PickingProcess.objects.create(
                    job=new_job,
                    picking_status='Waiting',  # Set the initial status to "Waiting"
                    notes='Initial picking status set.'  # Optional note
                )

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
    sort_order = request.GET.get('sort_order', 'newest')
    search_query = request.GET.get('search', '')
    if 'clear' in request.GET:
        search_query = ''

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


    if search_query:
        machines_query = machines_query.filter(job__job_name__icontains=search_query)


    # Adjust sorting based on user selection
    if sort_order == 'newest':
        machines_query = machines_query.order_by('-cnc_machine_id')  # Assuming 'created_at' is the field to sort by
    elif sort_order == 'oldest':
        machines_query = machines_query.order_by('cnc_machine_id')


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
        'total_mm18_quantity': totals['total_mm18_quantity'],
        'sort_order': sort_order,
        'search_query': search_query
    })






from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        return '/management/accounts/profile'







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
    picking_status_filter = request.GET.get('picking_status')
    sort_order = request.GET.get('sort_order', 'newest')
    search_query = request.GET.get('search', '')
    if 'clear' in request.GET:
        search_query = ''

    # Base queryset filtering jobs based on machining status
    picking_processes = PickingProcess.objects.select_related('job__CNCMachine').filter(
        ~Q(job__mm8_status='Waiting') | ~Q(job__mm18_status='Waiting')
    ).distinct()

    # Apply picking status filter if provided
    if picking_status_filter:
        if picking_status_filter == 'not_picked':
            picking_processes = picking_processes.exclude(picking_status='Picked')
        else:
            picking_processes = picking_processes.filter(picking_status=picking_status_filter)

    # Apply search query if provided
    if search_query:
        picking_processes = picking_processes.filter(
            Q(job__job_name__icontains=search_query) |
            Q(job__CNCMachine__machine_name__icontains=search_query)
        )

    # Sort order
    if sort_order == 'newest':
        picking_processes = picking_processes.order_by('-picking_id')
    elif sort_order == 'oldest':
        picking_processes = picking_processes.order_by('picking_id')

    # Pagination
    num_items = int(request.GET.get('num_jobs', 20))
    paginator = Paginator(picking_processes, num_items)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    context = {
        'page_obj': page_obj,
        'current_filter': picking_status_filter,
        'sort_order': sort_order,
        'search_query': search_query  # Ensure to pass the search query back to the template
    }
    return render(request, 'picking/picking_department.html', context)











@csrf_exempt
@login_required
@user_passes_test(is_picking)
def update_picking_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        picking_id = data.get('picking_id')  # Updated to use picking_id
        new_status = data.get('picking_status')

        picking_process = get_object_or_404(PickingProcess, pk=picking_id)  # Updated to fetch by pk
        picking_process.picking_status = new_status
        picking_process.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import PickingProcess
import json

# @csrf_exempt
# @login_required
# @user_passes_test(is_picking)
# def save_picking_notes(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         picking_id = data.get('picking_id')
#         notes = data.get('notes')
#         picking_status = data.get('picking_status')

#         picking_process = get_object_or_404(PickingProcess, picking_id=picking_id)
#         picking_process.notes = notes
#         picking_process.picking_status = picking_status
#         picking_process.save()

#         return JsonResponse({'status': 'success'})

#     return JsonResponse({'status': 'error'}, status=400)





@csrf_exempt
@login_required
@user_passes_test(is_picking)
def update_picking_notes(request, picking_id):
    if request.method == 'POST':
        picking_process = get_object_or_404(PickingProcess, pk=picking_id)
        notes = request.POST.get('picking_notes')
        picking_process.notes = notes
        picking_process.save()
        # Redirect to avoid POST on refresh and provide a success message if needed
        return redirect('picking_department')  # Replace 'some_view_name' with the name of the view to redirect to

    # Handle non-POST request if necessary
    return redirect('picking_department')  # Redirect or show an error




















from django.db.models import Prefetch
from .models import Workshop, PickingProcess, Job, Part
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q

@login_required
@user_passes_test(is_assembly)
def assembly_department(request):
    assembly_status_filter = request.GET.get('assembly_status', 'all')
    picking_status_filter = request.GET.get('picking_status', 'all')
    sort_order = request.GET.get('sort_order', 'newest')
    search_query = request.GET.get('search', '')

    if 'clear' in request.GET:
        search_query = ''

    # Start with the base query for workshops
    workshop_type = WorkshopTypes.objects.get(workshop_name="Assembly")
    workshops_query = Workshop.objects.filter(workshop_id=workshop_type).select_related(
        'part__sage_order_number'
    ).annotate(
        # Use timezone.now().date() instead of Now() and ensure the date subtraction works correctly
        days_old=ExpressionWrapper(
            Cast(timezone.now().date(), output_field=fields.DateField()) - F('part__sage_order_number__order_date'),
            output_field=DurationField()
        )
    )

    # Apply search filter
    if search_query:
        workshops_query = workshops_query.filter(
            Q(part__sage_order_number__delivery_postcode__icontains=search_query) |
            Q(part__sage_order_number__sage_order_number__icontains=search_query) |
            Q(part__product_code__product_code__icontains=search_query) |
            Q(part__product_code__product_description__icontains=search_query)
        )

    # Apply assembly status filter
    if assembly_status_filter != 'all':
        workshops_query = workshops_query.filter(assembly_status=assembly_status_filter)

    # Prepare a prefetch for PickingProcess linked through Job for each Part
    picking_prefetch = Prefetch('part__job__pickingprocess_set', queryset=PickingProcess.objects.all(), to_attr='picking_info')
    workshops_query = workshops_query.prefetch_related(picking_prefetch)

    # Apply sorting
    if sort_order == 'newest':
        workshops_query = workshops_query.order_by('-id')
    elif sort_order == 'oldest':
        workshops_query = workshops_query.order_by('id')

    # Pagination
    num_items = int(request.GET.get('num_items', 20))
    if 'show_more' in request.GET:
        num_items += 20

    paginator = Paginator(workshops_query.distinct(), num_items)
    page_obj = paginator.get_page(request.GET.get('page', 1))

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









from django.utils import timezone
from django.db.models import ExpressionWrapper, F, DurationField
from django.db.models.functions import Cast




@login_required
@user_passes_test(is_minikitchen)
def minikitchen_department(request):
    assembly_status_filter = request.GET.get('assembly_status', 'all')
    sort_order = request.GET.get('sort_order', 'newest')  # Default to 'newest'
    search_query = request.GET.get('search', '')  # Retrieve the search query

    if 'clear' in request.GET:
        search_query = ''


    workshop_type = WorkshopTypes.objects.get(workshop_name="Minikitchen")
    workshops_query = Workshop.objects.filter(workshop_id=workshop_type).select_related(
        'part__sage_order_number'
    ).annotate(
        # Use timezone.now().date() instead of Now() and ensure the date subtraction works correctly
        days_old=ExpressionWrapper(
            Cast(timezone.now().date(), output_field=fields.DateField()) - F('part__sage_order_number__order_date'),
            output_field=DurationField()
        )
    )

    if search_query:
        workshops_query = workshops_query.filter(
            Q(part__sage_order_number__delivery_postcode__icontains=search_query) |
            Q(part__sage_order_number__sage_order_number__icontains=search_query) |
            Q(part__product_code__product_code__icontains=search_query) |
            Q(part__product_code__product_description__icontains=search_query)
        )

    if assembly_status_filter == 'Waiting':
        workshops_query = workshops_query.filter(
            Q(assembly_status='Waiting') | Q(assembly_status='In Progress')
        )
    elif assembly_status_filter == 'Built':
        workshops_query = workshops_query.filter(assembly_status='Built')

    if sort_order == 'newest':
        workshops_query = workshops_query.order_by('-id')
    elif sort_order == 'oldest':
        workshops_query = workshops_query.order_by('id')

    num_items = int(request.GET.get('num_items', 20))
    if 'show_more' in request.GET:
        num_items += 20

    paginator = Paginator(workshops_query, num_items)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    
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
    workshops_query = Workshop.objects.filter(workshop_id=workshop_type).select_related(
        'part__sage_order_number'
    ).annotate(
        # Use timezone.now().date() instead of Now() and ensure the date subtraction works correctly
        days_old=ExpressionWrapper(
            Cast(timezone.now().date(), output_field=fields.DateField()) - F('part__sage_order_number__order_date'),
            output_field=DurationField()
        )
    )

    # Updated filter based on search query if provided
    if search_query:
        workshops_query = workshops_query.filter(
            Q(part__sage_order_number__delivery_postcode__icontains=search_query) |
            Q(part__sage_order_number__sage_order_number__icontains=search_query) |
            Q(part__product_code__product_code__icontains=search_query) |
            Q(part__product_code__product_description__icontains=search_query)
        )

    # Apply filters for assembly status
    if assembly_status_filter == 'Built':
        workshops_query = workshops_query.filter(assembly_status=assembly_status_filter)
    elif assembly_status_filter == 'Waiting':
        # Include both Waiting and In Progress statuses
        workshops_query = workshops_query.filter(
            Q(assembly_status='Waiting') | Q(assembly_status='In Progress')
        )

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
    page_obj = paginator.get_page(request.GET.get('page', 1))
    
    return render(request, 'assembly/plywood_department.html', {
        'page_obj': page_obj,
        'assembly_status_filter': assembly_status_filter,
        'sort_order': sort_order,
        'search_query': search_query,
    })












from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Sum, Q, F, ExpressionWrapper, fields
from django.utils import timezone
from .models import Upholstery

@login_required
@user_passes_test(is_upholstery)
def upholstery_department(request):
    assembly_status_filter = request.GET.get('assembly_status', 'all')
    search_query = request.GET.get('search', '')
    sort_order = request.GET.get('sort_order', 'newest')
    num_items = int(request.GET.get('num_items', 20))

    upholsteries_query = Upholstery.objects.select_related('part__sage_order_number').annotate(
        days_old=ExpressionWrapper(
            timezone.now().date() - F('part__sage_order_number__order_date'),
            output_field=fields.DurationField()
        )
    )

    # Apply the assembly status filter
    if assembly_status_filter == 'Built':
        upholsteries_query = upholsteries_query.filter(assembly_status='Goods Ready')
    elif assembly_status_filter == 'Waiting':
        upholsteries_query = upholsteries_query.exclude(assembly_status='Goods Ready')
    elif assembly_status_filter != 'all':
        upholsteries_query = upholsteries_query.filter(assembly_status=assembly_status_filter)

    # Apply the search query filter
    if search_query:
        upholsteries_query = upholsteries_query.filter(
            Q(part__product_code__icontains=search_query) |
            Q(part__sage_order_number__sage_order_number__icontains=search_query)
        )

    # Apply sorting based on the sort_order parameter
    if sort_order == 'newest':
        upholsteries_query = upholsteries_query.order_by('-upholstery_id')  # Sort by UpholsteryID descending for most recent
    elif sort_order == 'oldest':
        upholsteries_query = upholsteries_query.order_by('upholstery_id')  # Sort by UpholsteryID ascending for oldest

    paginator = Paginator(upholsteries_query, num_items)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    # Calculate the total value not built
    total_value_not_built = upholsteries_query.exclude(assembly_status='Goods Ready').aggregate(total=Sum('value'))['total'] or 0

    context = {
        'page_obj': page_obj,
        'assembly_status_filter': assembly_status_filter,
        'search_query': search_query,
        'sort_order': sort_order,
        'num_items': num_items,
        'total_value_not_built': total_value_not_built,
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
@login_required
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
from .models import Upholstery
from django.contrib.auth.decorators import login_required

@login_required
def update_upholstery_comment2(request, upholstery_id):
    if request.method == 'POST':
        comment2 = request.POST.get('comment2')

        upholstery = get_object_or_404(Upholstery, upholstery_id=upholstery_id)
        upholstery.comment2 = comment2
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

@login_required
def import_csv(request):
    if request.method == 'POST' and 'file' in request.FILES:
        csv_file = request.FILES['file']
        csvfile = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(csvfile)

        if 'Dept ' not in reader.fieldnames:
            raise ValueError("CSV file does not contain 'Dept' column or the column header is misspelled.")

        temp_customers = {}
        temp_orders = {}
        temp_parts = {}
        order_values = {}
        order_notes = {} 
        first_customer_per_order = {}


        # Mapping of department names to WorkshopTypes IDs
        workshop_ids = {
            'Assembly': 1,
            'MiniKitchenWorkshop': 2,
            'PlywoodWorkshop': 3
        }


        with transaction.atomic():
            for row in reader:
                # customer_name = row['Customer']
                sage_order_number = row['Sales Order']
                dept = row['Dept '].strip()


                if sage_order_number not in first_customer_per_order:
                    # If the customer field is not empty, store it as the first occurrence
                    if row['Customer'].strip():
                        first_customer_per_order[sage_order_number] = row['Customer'].strip()
                    else:
                        # If it's empty, initialize with None and expect to fill it later
                        first_customer_per_order[sage_order_number] = None
                # If the order number is already seen but no customer was stored yet
                elif not first_customer_per_order[sage_order_number] and row['Customer'].strip():
                    first_customer_per_order[sage_order_number] = row['Customer'].strip()

                # Use the first customer name encountered for this order number
                customer_name = first_customer_per_order[sage_order_number]
                if not customer_name:
                    continue




                if dept.lower() == 'default':
                    # Format the special code and its description
                    code = row['Product Code']
                    description = row['Description']
                    if sage_order_number not in order_notes:
                        order_notes[sage_order_number] = []
                    order_notes[sage_order_number].append(f"{code}: {description}")




                # Convert the 'Unit Price' to float and accumulate the total value per order
                unit_price_str = row.get('Unit Price', '0').strip()
                unit_price = 0.0
                if unit_price_str:
                    try:
                        unit_price = float(unit_price_str)
                    except ValueError:
                        print(f"Could not convert {unit_price_str} to float for order {sage_order_number}. Defaulting to 0.")

                order_values[sage_order_number] = order_values.get(sage_order_number, 0) + unit_price

                # Check if customer exists, if not create a new one
                customer, created = Customer.objects.get_or_create(name=customer_name)
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

                total_value = order_values.get(sage_order_number, 0)
                order, created = Order.objects.update_or_create(
                    sage_order_number=sage_order_number,
                    defaults={
                        'customer': customer,
                        'order_date': order_date,
                        'delivery_postcode': delivery_postcode,
                        'customer_postcode': customer_postcode,
                        'order_taken_by': order_taken_by,
                        'estimated_delivery_wkc': estimated_delivery_wkc,
                        'value': total_value,
                    }
                )
                if created:
                    temp_orders[order.sage_order_number] = {
                        'customer_id': customer.customer_id,
                        'order_date': order.order_date,
                        'value': total_value,
                    }

                if dept != 'Default':
                    # Retrieve or create the PartDescription instance
                    part_desc, created = PartDescription.objects.get_or_create(
                        product_code=row['Product Code'],
                        defaults={
                            # Set other required fields for PartDescription, if any
                        }
                    )

                    # Retrieve the order instance to link with the part
                    order_instance = Order.objects.get(sage_order_number=row['Sales Order'])

                    # Assuming 'Comment 1' and 'Comment 2' are columns in your CSV
                    comment_1 = row.get('Comment 1', '')  # Default to empty string if not present
                    comment_2 = row.get('Comment 2', '')  # Default to empty string if not present

                    # Create or update the part record
                    part, created = Part.objects.update_or_create(
                        sage_order_number=order_instance,
                        product_code=part_desc,
                        defaults={
                            'dept': row['Dept '],
                            'machine_status': None,  # Setting machine_status as null
                            'picking_status': None,  # Setting picking_status as null
                            'assembly_status': None,  # Setting assembly_status as null
                            'job': None,  # Setting job_id as null, assuming you have a Job model
                            'sage_comment1': comment_1,
                            'sage_comment2': comment_2,
                        }
                    )



                    # Now check if the part's department is upholstery
                    if row['Dept '].strip().lower() == 'upholstery':
                        # Create or update the Upholstery instance
                        # Assuming Upholstery model has a 'part' field that is a OneToOneField to the Part model
                        upholstery, created = Upholstery.objects.update_or_create(
                            part=part,
                            defaults={
                                'comments': row.get('Comment 1', ''),
                                'comment2': row.get('Comment 2', ''),
                                # Other fields are set to None as per your requirements
                                'value': None,
                                'pre_booked_date': None,
                                'routed_date': None,
                                'assembly_status': 'Waiting',
                                'assembly_notes': None,
                            }
                        )



                    dept = row['Dept '].strip()
                    workshop_type_id = workshop_ids.get(dept)

                    if workshop_type_id:
                        workshop_type = WorkshopTypes.objects.get(workshop_id=workshop_type_id)
                        # Create a new Workshop instance for the part
                        Workshop.objects.create(
                            workshop_id=workshop_type,
                            part=part,
                            assembly_status='Waiting',  # Set the default assembly_status to 'Waiting'
                            notes=''  # Add any default notes if needed
                        )







                    temp_parts[row['Product Code']] = {
                        'description': row['Description'],
                        'qty_ordered': row.get('Qty Ordered', 1),
                        'unit_price': unit_price,
                        'weight': row.get('Weight', 0.0),
                    }










                for sage_order_number, notes in order_notes.items():
                    formatted_notes = '; '.join(notes)  # Join all notes with a semicolon and space
                    order = Order.objects.get(sage_order_number=sage_order_number)
                    order.order_notes = formatted_notes
                    order.save()





        # Print temporary tables to the console
        print("Temporary Customers Table")
        for name, id in temp_customers.items():
            print(f"Customer Name: {name}, Customer ID: {id}")

        print("\nTemporary Orders Table")
        for order_num, order_data in temp_orders.items():
            print(f"Order Number: {order_num}, Order Data: {order_data}")

        print("\nTemporary Parts Table")
        for product_code, part_data in temp_parts.items():
            print(f"Product Code: {product_code}, Part Data: {part_data}")

        # Redirect or respond after processing
        return redirect('import_data')
    else:
        return HttpResponse('Failed to upload file', status=400)
    









from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile_view(request):
    # The context is automatically populated with the user instance for logged-in users
    return render(request, 'registration/profile.html')






















@login_required
@user_passes_test(is_cncmachining)
def job_detail_unedit(request, job_id):
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
    # Fetch workshop info linked to the job
    workshop_infos = Workshop.objects.filter(part__job=job).distinct()


    return render(request, 'machining/job_detail_unedit.html', {
        'job': job,
        'parts': parts,
        'orders': orders,
        'picking_infos': picking_infos,
        'cnc_infos': cnc_infos,
        'machining_status': machining_status,
        'workshop_infos': workshop_infos,
        'cnc_machines': cnc_machines
    })






from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Part

@login_required
def update_part_sage_comment1(request, part_id):
    if request.method == 'POST':
        sage_comment1 = request.POST.get('sage_comment1')

        part = get_object_or_404(Part, part_id=part_id)
        part.sage_comment1 = sage_comment1
        part.save()

        referer_url = request.META.get('HTTP_REFERER')
        if referer_url:
            return HttpResponseRedirect(referer_url)
        else:
            return redirect('profile')  # Adjust to your actual default redirect URL

    return redirect('profile')  # Adjust to your actual default redirect URL







@login_required
def update_part_sage_comment2(request, part_id):
    if request.method == 'POST':
        sage_comment2 = request.POST.get('sage_comment2')

        part = get_object_or_404(Part, part_id=part_id)
        part.sage_comment2 = sage_comment2
        part.save()

        referer_url = request.META.get('HTTP_REFERER')
        if referer_url:
            return HttpResponseRedirect(referer_url)
        else:
            return redirect('profile')  # Adjust to your actual default redirect URL

    return redirect('profile')  # Adjust to your actual default redirect URL





from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Order

def routing_view(request):
    num_items = int(request.GET.get('num_items', 10))

    parts_prefetch = Prefetch('part_set', queryset=Part.objects.select_related('product_code'))
    orders_query = Order.objects.prefetch_related(parts_prefetch).order_by('pk')

    paginator = Paginator(orders_query, num_items)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    # Iterate through orders to calculate days old for each part
    for order in page_obj:
        days_old = (now().date() - order.order_date).days
        for part in order.part_set.all():
            part.days_old = days_old  # Assigning days old to each part

    return render(request, 'routing/routing.html', {
        'page_obj': page_obj,
        'num_items': num_items,
    })