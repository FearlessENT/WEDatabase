# management/context_processors.py

def user_role_context(request):
    context = {
        'is_admin': request.user.groups.filter(name='Admin').exists(),
        'is_machinist': request.user.groups.filter(name='Machinist').exists() or request.user.groups.filter(name='Admin').exists(),
        'is_reception': request.user.groups.filter(name='Reception').exists() or request.user.groups.filter(name='Admin').exists(),
        'is_picking': request.user.groups.filter(name='Picking').exists() or request.user.groups.filter(name='Admin').exists(),
        'is_assembly': request.user.groups.filter(name='Assembly').exists() or request.user.groups.filter(name='Admin').exists(),
        # Add other roles as needed
    }
    return context
