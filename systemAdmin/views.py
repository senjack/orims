from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from .models import SystemAdmin
from django.http import HttpResponse
from .forms import *

"""
def index(request):
    return render(request, 'systemAdmin/extensions/login.html', context={})
"""

def adminLogin(request):
    try:
        request.session['user_id']
    except KeyError:
        loginForm = AdminLoginForm()
        context = {'form': loginForm}
        return render(request, 'systemAdmin/extensions/login.html', context)

    return HttpResponse("Already Logged in. Do you want to <a href='logout'>logout?</a>")


# ENTRY POINT : LOGIN ALGORITHM
# STEP1: Ensure to only allow Data sent using the post method.
@require_POST
# STEP2: Login process method definition starting point
def loginProcess(request):

    # STEP2.1: Define a custom template name to be rendered @ the end of the process
    template_name = 'systemAdmin/extensions/login.html'

    # STEP2.2: Creating a model form instance # sticks in a POST or renders empty form
    form = AdminLoginForm(request.POST or None)

    # STEP2.2: Test If form Exists and is Valid
    if form:
        # STEP2.2.1: Search database for a user with matching user name as that supplied.
        user = SystemAdmin.objects.get(system_admin_user_name=request.POST['username'])

        # if a user is found:
        # STEP2.2.2: Now check for whether passwords match, i.e. the one int the database
        # with the one supplied. .
        if user.system_admin_password == request.POST['password']:
            # If true:
            # STEP2.2.2: Set session for user.
            request.session['user_id'] = str(user.system_admin_user_name) + '(' + str(user.system_admin_id) + ')'
            # request.session['user_id'] = {'username': user.system_admin_user_name, 'id': user.system_admin_id}
            print(user)
            print(request.session['user_id'])
            return HttpResponse(request.session['user_id'])
        else:
            return redirect('login')
        # return render(request, 'systemAdmin/extensions/login.html', context={})

    #return redirect('home')
    # STEP2.3: If it tests otherwise than(form Exists and is Valid) return empty login form
    return render(request, template_name, {'form': form})
    # End : if form.is_valid():


# LOGOUT METHOD.
def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")

