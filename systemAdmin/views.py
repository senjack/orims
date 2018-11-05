from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from .forms import *
from orims.views import *
from orims.forms import *
from .models import SystemAdmin
from orims.meta import meta_data
from django.http.response import HttpResponse, JsonResponse, Http404
from django.http.request import HttpRequest
from django.core.files import uploadedfile
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import check_password
from django.contrib.auth import views

"""
def index(request):
    return render(request, 'systemAdmin/extensions/login.html', context={})
"""


def signup(request):
    # STEP 1.0: Test whether POST method is used.
    # POST method is needed for Form Data security
    if request.method == 'POST':
        # STEP 1.1: If the POST method was used, then create and set Variables(filled up form and template).
        # Create a new form instance(f)
        f = AdminSignUpForm(request.POST)
        # Create a template instance
        t = 'systemAdmin/extensions/signup.html'

        # STEP 1.2: Check for form validity(status)
        if f.is_valid():
            # STEP 1.2.1: If form is valid, then save data in the form and and then clear the signUp form,
            #  by creating a new empty signUp form instance.
            f.save()
            f = AdminSignUpForm()

            # STEP 1.2.2: Now return the empty Signup form with success message alert initiated.
            return render(request, t, {'form': f,'display_success':True})
        # End of if f.is_valid():

    else:
        # STEP 1.2.1: If the POST method was not used, then Drop or clear up that insecure data,
        # By creating an empty signUp form instance.
        # OR in case of first signup instance, Prepare an empty signup form.
        f = AdminSignUpForm()
    # End of if request.method == 'POST':

    # STEP 2.0: In case of first signup instance, Return an empty SignUp form.
    return render(request, 'systemAdmin/extensions/signup.html', {'form': f})
# End of function signup():


def login(request):
    # Set login template.
    t = 'systemAdmin/extensions/login.html'

    # If the Request POST variable has data in it, Create a filled up Login form instance(f).
    # Otherwise set f to nothing.
    f = AdminLoginForm(request.POST or None)

    # set f as a value to the key 'form' of the context object to be passed on to any returned template
    context = {'form':f}

    # Test for whether POST method was used
    if request.method == 'POST':
        # In case the request.POST variable has some data, Test for validity of the passed data.
        if f.is_valid:
            # If data in the Request.POST variable is valid, fetch user name from the form.
            username = request.POST['username'].lower()

            # Check whether there is any user with the supplied user name.
            u = SystemAdmin.objects.filter(system_admin_user_name= username)
            if not u.count():
                # In case there is no user with the supplied user name set username error
                uname_error = "There is no User with the supplied Username. \
                Please Enter your correct Username and Try again."
                context.update({'username_error': uname_error})

                # Terminate the login process and throw username error.
                return render(request, t, context)
            # End of if not u.count():

            # In case there is a user with the supplied username,
            # fetch the supplied password form the submitted form.
            password = request.POST['password']
            u1 = SystemAdmin.objects.get(system_admin_user_name= username)

            # Compare the supplied password with that of the filtered user from the database.
            p = u1.get_password(password)
            if not p:
                # In case the two password don't tally or match, set password error
                password_error = "Invalid password. \
                Please Enter your correct Password and Try again."
                context.update({'password_error': password_error})
                # Terminate the login process and throw password error
                return render(request, t, context)
            # End of if not p:

            # In case the two passwords match, then the authentication process was successful.
            # Hence set or start the user session for admin.
            user = u1.get_user_id()
            request.session['user_admin'] = user

            # After the system admin user session has been successfully set, then redirect to System-admin home.
            return redirect('systemAdmin:home')
        # End of if f.is_valid:
    else:
        # In case no data was submitted,.
        try:
            # Test for any logged in user.
            if request.session['user_admin']:
                # In case of a logged in user, redirect to System admin home.
                return redirect('systemAdmin:home')
        except KeyError:
            # Else create an empty login form for logging in.
            f = AdminLoginForm()
        # End of try:

        context.update({'form': f})
    # End of: if request.method == 'POST':

    # Return the new created empty login form.
    return render(request, t, context)
# End of function login():


# SYSTEM ADMIN HOME PAGE BUILDER
def home(request):
    # STEP1.0.0: Set home template and create an empty context object.
    t = 'systemAdmin/extensions/home.html'
    context = {}
    # STEP1.1: Test for session, to determine currently logged in user.
    try:
        if request.session['user_admin']:
            # if user is logged in, build home page.
            # create new user instance
            user = request.session['user_admin']

            # Set session data for the new user
            set_session_data(request, user)

            # Fetch and set all service units created or managed by the current user.
            units = fetch_units_for_user(user)
            context.update({'units': units})

            # Set admin panel options
            context.update({'options': admin_panel_options(active='dashboard')})

            # Build and return the home client view template with the set units for the user
            return render(request, t, context)
        else:
            # if no user is logged in, try Logging in.
            return redirect('systemAdmin:login')
        # End of if request.session['user_admin']:
    except KeyError:
        # In case  testing for the logged in user fails, try nothing,
        pass
    # End of try:
    # Just try logging in.
    return redirect('systemAdmin:login')
# End of function home():


# SERVICE UNITS HANDLING METHOD
def serviceUnits(request, deleted = None):
    # STEP1.0.0: Set template and create an empty context object.
    t = 'systemAdmin/extensions/service_units.html'
    context = {}
    f = UnitCreationForm(request.POST or None)

    # STEP1.1: Test for session, to determine currently logged in user.
    try:
        if request.session['user_admin']:
            # if user is logged in, build the required page.
            # create new user instance
            user = request.session['user_admin']

            # Set session data for the new user
            set_session_data(request, user)

            # Fetch and set all service units created or managed by the current user.
            units = fetch_units_for_user(user)

            # Set admin panel options
            context.update({'options': admin_panel_options(active='unit')})

            if (deleted == 'deleted') or (request.GET and request.GET['user'] == 'system-admin' and request.GET['level'] == 'system_admin' and request.GET['action'] == 'view_units'):
                t = 'systemAdmin/extensions/service_units.html'
                context.update({'units': units})
                context.update({'section_title_info': 'A list of All Service units you manage.'})
                context.update({'toggle_title1': 'Select this Service unit for more Management options'})
                context.update({'btn1_value': 'glyphicon glyphicon-thumbs-up'})
                context.update({'toggle_title2': 'Edit this Service unit\'s Information'})
                context.update({'btn2_value': 'glyphicon glyphicon-pencil clr-gre'})
                context.update({'toggle_title3': 'Delete this Service unit'})
                context.update({'btn3_value': 'glyphicon glyphicon-trash clr-gre1'})
                context.update({'branches': ''})
                context.update({'display_unit_selection_list': True})

                if deleted == 'deleted':
                    context.update({'unit_delete_success': True})
                # End if
                return render(request, t, context)
            # End if

            if request.GET and request.GET['user'] == 'system-admin' and request.GET['level'] == 'system_admin':
                if request.GET['mode'] == 'load_form':
                    t = 'systemAdmin/extensions/mono_page.html'
                    if request.GET['action'] == 'create_unit':
                        context.update({'units': units})
                        build_unit_registration_form(context=context)

                        if request.method == 'POST':
                            if f.is_valid():
                                pass
                        else:
                            context.update({'form': f})

                elif request.GET['action'] == 'cancel_unit_creation' and request.GET['mode'] == 'hide_form':
                    # Empty all form fields:
                    f = UnitCreationForm()
                    return redirect('systemAdmin:serviceUnits')

                # Build and return the required page
                return render(request, t, context)
            else:
                # In case of no GET request, just load service unit options
                return render(request, t, context)
        else:
            # if no user is logged in, try Logging in.
            return redirect('systemAdmin:login')
        # End of if request.session['user_admin']:
    except KeyError:
        # In case  testing for the logged in user fails, try nothing,
        pass
    # End of try:
    # Just try logging in.
    return redirect('systemAdmin:login')
# End of officeAccounts() Method


# SERVICE UNIT CREATION VIEW METHOD
def createUnit(request):
    # STEP1.0.0: Set template and create an empty context object.
    t = 'systemAdmin/extensions/mono_page.html'
    context = {}
    f = UnitCreationForm(request.POST, request.FILES or None)

    # STEP1.1: Test for session, to determine currently logged in user.
    try:
        if request.session['user_admin']:
            # if user is logged in, build the required page.
            # create new user instance
            user = request.session['user_admin']

            # Set session data for the new user
            set_session_data(request, user)

            if request.POST:
                if f.is_valid():
                    # STEP 1: Create a form instance which is not to be saved instantly
                    instance = f.save(commit=False)

                    # STEP 2: If current user is Admin,
                    # Attach current user as system admin
                    us = SystemAdmin.objects.get(system_admin_id = user)
                    instance.system_admin_id = us
                    unit_creation_success = False

                    # Check for whether There is already a unit registered with the same name
                    name1 = f.cleaned_data["unit_name"]
                    name2 = None
                    try:
                        name2 = ServiceUnit.objects.get(unit_name=name1)
                    except:
                        pass

                    if name2 is not None:
                        context.update({'unit_name_matched': True})
                    else:
                        # STEP 3: Create / save service unit
                        instance.save()

                        # Step 4: Create default Branch and name it 'Main Branch'
                        # 4.1: Create instance for the newly created service unit.
                        unit = ServiceUnit.objects.get(unit_id=instance.unit_id)
                        # 4.2: Create a unit object to be sent to the client together with the form
                        context.update({'unit': unit})
                        # 4.3: call Branch creation method
                        b = create_branch(service_unit_id=unit, branch_name='Main', branch_level='main')
                        b

                        # Step 5: Create default Department and name it 'Reception Department'
                        # 5.1: Create instance for the newly created Branch.
                        branch = Branch.objects.get(branch_id=b)
                        # 5.2: call Department creation method
                        d = create_department(branch_id=branch,
                                              dept_name='Reception',
                                              dept_description ="""This is the the Receiption department, Under which the following are expected.\n
                        I.	Sending official appointment request to official\n
                        II.	Assigning appointment dates to public\n
                        III.	Contacting person who placed appointment once official approves appointment.\n
                        IV.	Canceling appointments
                        """,)
                        d

                        # Step 6: Create default Office and name it 'Office of the Receptionist'
                        # 6.1: Create instance for the newly created Department.
                        department = Department.objects.get(department_id=d)
                        # 6.2: call Department creation method
                        o = create_office(department_id=department,
                                          office_name='Receptionist',
                                          working_time='Standard',
                                          office_description ="""This is the the Office of the Receptionist, Under which the following are expected.\n
                        I.	Sending official appointment request to official\n
                        II.	Assigning appointment dates to public\n
                        III.	Contacting person who placed appointment once official approves appointment.\n
                        IV.	Canceling appointments
                        """,)
                        o

                        print("\nService unit registered succesfully : " + str(instance))

                        # Turn on flags to enable loading unit update form
                        unit_creation_success = True
                        context.update({'unit_creation_success': True})
                        # request.session['unit_update'] = instance.unit_id
                        updateUnit(request, unit_id=instance.unit_id)

                    context.update(build_unit_update_form(context))
                    # Check for whether a flag to enable loading unit update form is on
                    if unit_creation_success:
                        f = UnitCreationForm(instance=instance)
                    else:
                        build_unit_registration_form(context=context)

                    context.update({'form': f})
                    return render(request, t, context)
            else:
                return HttpResponse("<font color = 'red'><b>Un Expected Error</b></font>")
            # Build and return the required page
            return render(request, t, context)
        else:
            # if no user is logged in, try Logging in.
            return redirect('systemAdmin:login')
        # End of if request.session['user_admin']:
    except KeyError:
        # In case  testing for the logged in user fails, try nothing,
        pass
    # End of try:
    # Just try logging in.
    return redirect('systemAdmin:login')


# LOAD SERVICE UNIT UPDATE FORM
def editUnit(request,unit_id = None):
    # STEP1.0.0: Set template and create an empty context object.
    t = 'systemAdmin/extensions/mono_page.html'
    context = {}

    # STEP1.1: Test for session, to determine currently logged in user.
    try:
        if request.session['user_admin']:
            # if user is logged in, build the required page.
            # create new user instance
            user = request.session['user_admin']

            # Set session data for the new user
            set_session_data(request, user)
            unit = get_object_or_404(ServiceUnit,unit_id=unit_id)

            if unit:
                f = UnitCreationForm(instance=unit)
                context.update({"edit_unit":True})
                context.update(build_unit_update_form(context))

                # Create a unit object to be sent to the client together with the form
                context.update({'unit': unit})
                context.update({'form': f})

                return render(request, t, context)
            else:
                # If no Service unit matches the given query,
                # Just Load the standard HTTP 404 page.
                return Http404()
        else:
            # if no user is logged in, try Logging in.
            return redirect('systemAdmin:login')
        # End of if request.session['user_admin']:
    except KeyError:
        # Just try logging in.
        return redirect('systemAdmin:login')


# SERVICE UNIT UPDATE VIEW METHOD
def updateUnit(request,unit_id = None):
    # STEP1.0.0: Set template and create an empty context object.
    t = 'systemAdmin/extensions/mono_page.html'
    context = {}
    # STEP1.1: Test for session, to determine currently logged in user.
    try:
        if request.session['user_admin']:
            # if user is logged in, build the required page.
            # create new user instance
            user = request.session['user_admin']
            # Set session data for the new user
            set_session_data(request, user)

            # return HttpResponse("<font color = 'green'><b>Found</b></font>")

            if request.POST:
                    unit = get_object_or_404(ServiceUnit, unit_id=unit_id)
                    f = UnitCreationForm(request.POST, request.FILES or None, instance=unit)

                    # unit = ServiceUnit.objects.get(unit_id=request.session['unit_update'])
                    if unit and f.is_valid():
                        f.save()
                    else:
                        # If no Service unit matches the given query, Or form Data not validated,
                        # Just Load the standard HTTP 404 page.
                        return Http404()

                   # Turn on flags to enable loading unit update form
                    unit_update_success = True
                    context.update({'unit_update_success': True})
                    if unit_update_success:
                        context.update(build_unit_update_form(context))
                        # Create a unit object to be sent to the client together with the form
                        context.update({'unit': unit})
                        context.update({'form': f})

                    return render(request, t, context)
            else:
                return HttpResponse("<font color = 'red'><b>Un Expected Error</b></font>")
        else:
            # if no user is logged in, try Logging in.
            return redirect('systemAdmin:login')
        # End of if request.session['user_admin']:
    except KeyError:
        # In case  testing for the logged in user fails, try nothing,
        pass
    # End of try:
    # Just try logging in.
    return redirect('systemAdmin:login')


# DELETE SERVICE UNIT
def deleteUnit(request,unit_id = None):
    # STEP1.0.0: Set template and create an empty context object.
    t = 'systemAdmin/extensions/mono_page.html'
    context = {}
    # STEP1.1: Test for session, to determine currently logged in user.
    try:
        if request.session['user_admin']:
            # if user is logged in, build the required page.
            # create new user instance
            user = request.session['user_admin']
            # Set session data for the new user
            set_session_data(request, user)
            unit = get_object_or_404(ServiceUnit,unit_id=unit_id)

            # Set admin panel options
            context.update({'options': admin_panel_options(active='dashboard')})

            if unit:
                unit.delete()

                # Turn on flags to enable loading unit update form
                unit_delete_success = True
                context.update({'unit_delete_success': True})
                if unit_delete_success:
                    # Create a unit object to be sent to the client together with the form
                    context.update({'unit': unit})
                    return redirect('systemAdmin:serviceUnits',deleted = 'deleted')
                    #return render(request, t, context)
                else:
                    return HttpResponse("<font color = 'red'><b>Error Encountered while Deleting the Service Unit</b></font>")
            else:
                # If no Service unit matches the given query,
                # Just Load the standard HTTP 404 page.
                return Http404()

            return render(request, t, context)
        else:
            # if no user is logged in, try Logging in.
            return redirect('systemAdmin:login')
        # End of if request.session['user_admin']:
    except KeyError:
        # Just try logging in.
        return redirect('systemAdmin:login')


# LOAD ADMIN UPDATE FORM
def editAdmin(request):
    # STEP1.0.0: Set template and create an empty context object.
    t = 'systemAdmin/extensions/mono_page.html'
    context = {}
    # STEP1.1: Test for session, to determine currently logged in user.
    try:
        if request.session['user_admin']:
            # if user is logged in, build the required page.
            # create new user instance
            user = request.session['user_admin']
            # Set session data for the new user
            set_session_data(request, user)
            admin = get_object_or_404(SystemAdmin,system_admin_id=user)
            if admin:
                # updateAdmin(request, admin_id)
                f = AdminUpdateForm(instance=admin) or None
                context.update(build_admin_update_form(context))

                # Create admin object to be sent to the client together with the form
                context.update({'admin': admin})
                context.update({'form': f})
                print(f)

                return render(request, t, context)
###
            else:
                pass
                # method coming soon
        else:
            # if no user is logged in, try Logging in.
            return redirect('systemAdmin:login')
        # End of if request.session['user_admin']:
    except KeyError:
        # Just try logging in.
        return redirect('systemAdmin:login')


# ADMIN UPDATE
def updateAdmin(request,admin_id = None):
    # STEP1.0.0: Set template and create an empty context object.
    t = 'systemAdmin/extensions/mono_page.html'
    context = {}
    # STEP1.1: Test for session, to determine currently logged in user.
    try:
        if request.session['user_admin']:
            # if user is logged in, build the required page.
            # create new user instance
            user = request.session['user_admin']
            # Set session data for the new user
            set_session_data(request, user)

            if request.POST:
                    admin = get_object_or_404(SystemAdmin, system_admin_id=admin_id)
                    f = AdminUpdateForm(request.POST, request.FILES or None, instance=admin)

                    if admin and f.is_valid():
                        f.save()
                        # return HttpResponse("<font color = 'green'><b>Profile Updated! Successfully</b></font>")

                   # Turn on flags to enable loading admin update form
                    admin_update_success = True
                    context.update({'admin_update_success': True})
                    if admin_update_success:
                        context.update(build_admin_update_form(context))
                        # Create admin object to be sent to the client together with the form
                        context.update({'admin': admin})
                        context.update({'form': f})

                    return render(request, t, context)
            else:
                return HttpResponse("<font color = 'red'><b>Un Expected Error</b></font>")
        else:
            # if no user is logged in, try Logging in.
            return redirect('systemAdmin:login')
        # End of if request.session['user_admin']:
    except KeyError:
        # In case  testing for the logged in user fails, try nothing,
        pass
    # End of try:
    # Just try logging in.
    return redirect('systemAdmin:login')


def build_admin_update_form(context=None):
    context.update({'update_admin': True})
    context.update({'form_title': 'Profile Update form'})
    context.update({'form_prompt_message': 'Edit and update your profile.'})
    context.update({'submit_button_caption': 'Update'})
    context.update({'toggle_title1': 'Click to Update your profile'})
    context.update({'toggle_title2': 'Click to Cancel Update Process'})
    context.update({'action': 'update_admin'})

    # Set admin panel options
    context.update({'options': admin_panel_options(active='profile')})

    return context


# USER ACCOUNTS MANAGEMENT OPTIONS PAGE BUILDER
def userAccounts(request):
    # STEP1.0.0: Set template and create an empty context object.
    t = 'systemAdmin/extensions/user_accounts.html'
    context = {}

    # STEP1.1: Test for session, to determine currently logged in user.
    try:
        if request.session['user_admin']:
            # if user is logged in, build the required page.
            # create new user instance
            user = request.session['user_admin']
            # Set session data for the new user
            set_session_data(request, user)

            # Set admin panel options
            context.update({'options': admin_panel_options(active='profile')})

            # Build and return the required page
            return render(request, t, context)
        else:
            # if no user is logged in, try Logging in.
            return redirect('systemAdmin:login')
        # End of if request.session['user_admin']:
    except KeyError:
        # In case  testing for the logged in user fails, try nothing,
        pass
    # End of try:
    # Just try logging in.
    return redirect('systemAdmin:login')
# End of userAccounts() Method


# APPOINTMENT RECORDS MANAGEMENT OPTIONS PAGE BUILDER
def appointments(request):
    # STEP1.0.0: Set template and create an empty context object.
    t = 'systemAdmin/extensions/appointments.html'
    context = {}

    # STEP1.1: Test for session, to determine currently logged in user.
    try:
        if request.session['user_admin']:
            # if user is logged in, build the required page.
            # create new user instance.
            user = request.session['user_admin']
            # Set session data for the new user
            set_session_data(request, user)
            # Fetch and set all service units created or managed by the current user.
            units = fetch_units_for_user(user)
            branches = []
            for unit in units:
                branches.append(fetch_branches_for_units(unit.unit_id))
            branches = branches

            context.update({'units': units})
            context.update({'branches': branches})
            context.update({'section_title_info': 'You can view appointments for the entire Service unit, or browse for Branches under it.'})
            context.update({'toggle_title1': 'View Appointments for this entire Service unit'})
            context.update({'btn1_value': 'glyphicon glyphicon-eye-open'})
            context.update({'toggle_title2': 'Browse Branches under this Service unit'})
            context.update({'btn2_value': 'glyphicon glyphicon-option-horizontal clr-grn'})
            # Build and return the required page
            return render(request, t, context)
        else:
            # if no user is logged in, try Logging in.
            return redirect('systemAdmin:login')
        # End of if request.session['user_admin']:
    except KeyError:
        # In case  testing for the logged in user fails, try nothing,
        pass
    # End of try:
    # Just try logging in.
    return redirect('systemAdmin:login')
# End of appointments() Method


# LOGOUT METHOD.
def logout(request):
    """ THE LOGOUT PROCESS """
    try:
        if request.session['user_admin']:
            # Logout any system-admin currently logged in
            del request.session['user_admin']
        # END: if request.session['user_admin']:

        if request.session['user_receptionist']:
            # Logout any Receptionist currently logged in
            del request.session['user_staff']
        # END: if request.session['user_receptionist']:

        if request.session['user_staff']:
            # Logout any official currently logged in
            del request.session['user_staff']
        # END: if request.session['user_staff']:

        if request.session['current_time']:
            # Delete the current time session
            del request.session['current_time']
        # END: if request.session['current_time']:

        # After logging out any possible user, redirect to login page
        return redirect('systemAdmin:login')
    except KeyError:
        # OTHERWISE. redirect to login page
       return redirect('systemAdmin:login')
    # END OF: try
# End of function logout():


# CHECK ADMIN LOGIN STATUS EVERY TIME BEFORE LOADING ANY TEMPLATE
def loggedin(request, template, data_feed):
    # STEP1.0: Receive and store passed template(template) in local variable t.
    t = template

    # STEP1.0: Receive and store passed data feed in local variable df.
    df = data_feed

    # STEP2.0: Test for running session, to determine if there is any logged in user(user_admin).
    # Using the try concept, to handle omissions in case no session instance is found.
    try:
        # if there is any user logged in, return appropriate template and data_feeds.
        if request.session['user_admin']:
            return render(request, t,)

        # if no user is logged in, redirect to Login page.
        else:
            return redirect('systemAdmin:login')
        # End if request.session['user_admin']:

    # Throw keyError as exception just in case.
    except KeyError:
        # If all is well, just do nothing.
        pass
    # Failure to successfully execute this code, just load the home page.
    return redirect('systemAdmin:login')
    # End of try
# End of function loggedin():


# A method set admin panel options
def admin_panel_options(active='dashboard'):
    dashboard = {'name':'Dashboard','link': 'systemAdmin:home', 'glyphicon': 'glyphicon-dashboard', 'active': ''}
    unit = {'name':'Service Units','link': 'systemAdmin:serviceUnits', 'glyphicon': 'glyphicon-home', 'active': ''}
    profile = {'name':'Admin Profile','link': 'systemAdmin:userAccounts', 'glyphicon': 'glyphicon-user', 'active': ''}
    monitor = {'name':'Monitoring Tool','link': '#', 'glyphicon': 'glyphicon-eye-open', 'active': ''}
    documents = {'name':'Documents','link': '#', 'glyphicon': 'glyphicon-book', 'active': ''}
    settings = {'name':'General Settings','link': '#', 'glyphicon': 'glyphicon-cog', 'active': ''}

    if active == 'dashboard':
        dashboard.update({'active': 'active-pill'})
    elif active == 'unit':
        unit.update({'active': 'active-pill'})
    elif active == 'profile':
        profile.update({'active': 'active-pill'})
    elif active == 'monitor':
        monitor.update({'active': 'active-pill'})
    elif active == 'documents':
        documents.update({'active': 'active-pill'})
    elif active == 'settings':
        settings.update({'active': 'active-pill'})
    else:
        pass

    a = [
        dashboard,unit,profile,monitor,documents,settings
        # {'dashboard':dashboard},
        # {'unit':unit},
        # {'profile':profile},
        # {'monitor':monitor},
        # {'documents':documents},
        # {'settings':settings}
    ]
    return a


# Fetch user details based on session admin id
# This data is always to be fetched frequently before any action.
# This is because, in case the user data is updated, the session is updated too.
def set_session_data(request, uid):
    if uid:
        u = get_object_or_404(SystemAdmin, system_admin_id=uid)
        request.session['app'] = 'orims.com'
        request.session['user_admin'] = uid

        request.session['username']= u.system_admin_user_name
        request.session['role']= 'Administrator'
        request.session['email']= u.system_admin_email
        try:
            request.session['profile_photo'] = u.system_admin_profile_photo.url
        except:
            pass

        t= timezone.now().date().year
        # 'year': timezone.now().date().year,
        # 'month': timezone.now().date().month,
        # 'day': timezone.now().date().day,
        # 'weekday': timezone.now().date().isoweekday(),
        # 'hour': timezone.now().time().hour,
        # 'minute': timezone.now().time().minute,
        # 'second': timezone.now().time().second,
        # 'microsecond': timezone.now().time().microsecond,
        # 'meridian': timezone.now().time(),
        request.session['current_time'] = t
        request.session['meta'] = meta_data
# End of def set_ssession_data()
