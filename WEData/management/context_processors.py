# management/context_processors.py

def user_role_context(request):
    context = {
        'is_admin': request.user.groups.filter(name='Admin').exists(),
        'is_machinist': request.user.groups.filter(name='Machinist').exists(),
        # Add other roles as needed
    }
    return context
