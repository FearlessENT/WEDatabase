from django.contrib import admin
from .models import Customer, Order, PartDescription, Part, OrdertoJobBridge, CNCMachineDescription, CNCMachine, PickingProcess, WorkshopTypes, Workshop

# Register your models here.
admin.site.register(Customer)
admin.site.register(PartDescription)
admin.site.register(Part)
admin.site.register(OrdertoJobBridge)
admin.site.register(CNCMachineDescription)
admin.site.register(CNCMachine)
admin.site.register(PickingProcess)
admin.site.register(WorkshopTypes)
admin.site.register(Workshop)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('sage_order_number', 'customer', 'order_date', 'value')
    search_fields = ('sage_order_number', 'customer__name')
