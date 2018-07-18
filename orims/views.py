from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import *


def index(request):
    a = ServiceUnit.objects.all()
    print(a)
    return render(request, 'orims/base/index.html', context={'title': 'System Administrator'})

