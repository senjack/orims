from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import *


def index(request):
    a = ServiceUnit.objects.all()
    print(a)
    return render(request, 'orims/base/index.html', context={'title': 'System Administrator'})


# A method to return all service units
def fetch_all_units(request):
    # Fetch and return all units from the  database
    return ServiceUnit.objects.all()

# A method to return all service units managed by a user
def fetch_units_for_user(user_id):
    filtered_units = ServiceUnit.objects.filter(system_admin_id=user_id)
    return filtered_units
