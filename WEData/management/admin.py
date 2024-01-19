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



from django.contrib import admin
from .models import Profile, CNCMachine

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'assigned_cnc_machine']
    search_fields = ['user__username']
    list_filter = ['assigned_cnc_machine']


# admin.site.register(Profile, ProfileAdmin)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
