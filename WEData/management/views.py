from django.shortcuts import render
from .models import Order
from django.db.models import Q

def order_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        orders = Order.objects.filter(Q(sage_order_number__icontains=search_query) | Q(customer__name__icontains=search_query))
    else:
        orders = Order.objects.all()
    return render(request, 'management/order_list.html', {'orders': orders, 'search_query': search_query})



def order_detail(request, sage_order_number):
    order = Order.objects.get(sage_order_number=sage_order_number)
    # Fetch additional related data as needed
    return render(request, 'management/order_detail.html', {'order': order})
