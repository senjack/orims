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


# A method to create a branch
def create_branch(service_unit_id, branch_name, branch_level):
    branch = Branch(unit_id=service_unit_id, branch_name=branch_name, branch_level=branch_level)
    branch.save()
    return branch.branch_id


# A method to create a Department
def create_department(branch_id,dept_name,dept_description):
    department = Department(branch_id=branch_id,
                            department_name=dept_name,
                            department_description=dept_description,
                            )
    department.save()
    return department.department_id


# A method to create an office
def create_office(department_id,office_name,working_time,office_description):
    office = Office(department_id=department_id,
                    office_name=office_name,
                    office_description=office_description,
                    office_working_time=working_time
                    )
    office.save()
    return office.office_id


# A method to return all Branches under a service unit managed by a user
def fetch_branches_for_units(unit_id):
    filtered_branches = Branch.objects.filter(unit_id=unit_id)
    return filtered_branches

# A method to return all Branches
def fetch_all_branches():
    branches = Branch.objects.all()
    return branches

def build_unit_registration_form(context=None):
    context.update({'create_unit': True})
    context.update({'form_title': 'Service unit Registration form'})
    context.update({'form_prompt_message': 'Register Ministry, Organisation, Business, Firm, ...'})
    context.update({'submit_button_caption': 'Register Unit'})
    context.update({'toggle_title1': 'Click to Register Service Unit'})
    context.update({'toggle_title2': 'Click to Cancel Service Unit Registration Process'})
    context.update({'action': 'create_unit'})
    return context

def build_unit_update_form(context=None):
    context.update({'update_unit': True})
    context.update({'form_title': 'Service unit Update form'})
    context.update({'form_prompt_message': 'Edit and update this Service Unit Information.'})
    context.update({'submit_button_caption': 'Update'})
    context.update({'toggle_title1': 'Click to Update Service Unit Information'})
    context.update({'toggle_title2': 'Click to Cancel Service Unit information Update Process'})
    context.update({'action': 'update_unit'})
    return context