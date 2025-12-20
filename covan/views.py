from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def is_covan(user):
    return user.groups.filter(name='CO_VAN').exists()

@login_required
@user_passes_test(is_covan)
def dashboard(request):
    return render(request, 'covan/dashboard.html')
