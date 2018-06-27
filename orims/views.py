from django.shortcuts import render
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
# from .models import <PENDING>

def index(request):
    return HttpResponse("Hello, world. You're welcome @ the orims index page.<br/>Page is still under construction")