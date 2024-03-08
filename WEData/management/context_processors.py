# management/context_processors.py

def user_role_context(request):
    context = {
        'is_admin': request.user.groups.filter(name='Admin').exists(),
        'is_picking': request.user.groups.filter(name='Picking').exists() or request.user.groups.filter(name='Admin').exists(),
        'is_assembly': request.user.groups.filter(name='Assembly').exists() or request.user.groups.filter(name='Admin').exists(),
        'is_cncmachining': request.user.groups.filter(name='CNCMachining').exists() or request.user.groups.filter(name='Admin').exists(),
        'is_orders': request.user.groups.filter(name='Orders').exists() or request.user.groups.filter(name='Admin').exists(),
        'is_job': request.user.groups.filter(name='Jobs').exists() or request.user.groups.filter(name='Admin').exists(),
        'is_assembly': request.user.groups.filter(name='Assembly').exists() or request.user.groups.filter(name='Admin').exists(),
        'is_upholstery': request.user.groups.filter(name='Upholstery').exists() or request.user.groups.filter(name='Admin').exists(),
        'is_plywood': request.user.groups.filter(name='Plywood').exists() or request.user.groups.filter(name='Admin').exists(),
        'is_minikitchen': request.user.groups.filter(name='Minikitchen').exists() or request.user.groups.filter(name='Admin').exists(),
        'is_misc': request.user.groups.filter(name='Misc').exists() or request.user.groups.filter(name='Admin').exists(),
        'is_import': request.user.groups.filter(name='Import').exists() or request.user.groups.filter(name='Admin').exists(),
        'is_routing': request.user.groups.filter(name='Routing').exists() or request.user.groups.filter(name='Admin').exists(),

        # Add other roles as needed
    }
    return context
