from django.shortcuts import render

from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world. You're welcome @ the orims index page.<br/>Page is still under construction")