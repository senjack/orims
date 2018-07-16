from django.contrib import admin

from .models import *


class ManageAvails(admin.ModelAdmin):
    fieldsets = [
        ('Staffs Available for Appointments', {'fields': ['availer']}),
        (None, {'fields': ['availed']}),
        (None, {'fields': ['session_start']}),
        (None, {'fields': ['session_stop']}),
    ]


class ManageStaffSchedule(admin.ModelAdmin):
    fieldsets = [
        ('Staffs Schedule Details', {'fields': ['staff_id']}),
        (None, {'fields': ['sch_date']}),
        (None, {'fields': ['effect_date']}),
        (None, {'fields': ['start_time']}),
        (None, {'fields': ['end_time']}),
        (None, {'fields': ['appointment_id']}),
        (None, {'fields': ['sch_reason']}),
    ]


class ManageAppointment(admin.ModelAdmin):
    fieldsets = [
        ('Appointments Details', {'fields': ['staff_id']}),
        (None, {'fields': ['appointment_id']}),
        (None, {'fields': ['placement_time']}),
        (None, {'fields': ['start_time']}),
        (None, {'fields': ['stop_time']}),
        (None, {'fields': ['reason']}),
        (None, {'fields': ['appointment_mode']}),
    ]


class ManageClient(admin.ModelAdmin):
    fieldsets = [
        ('Client Details', {'fields': ['appointment_id']}),
        (None, {'fields': ['client_first_name']}),
        (None, {'fields': ['client_last_name']}),
        (None, {'fields': ['client_contact']}),
        (None, {'fields': ['client_location_district']}),
        (None, {'fields': ['client_location_town']}),
    ]


admin.site.register(Avails, ManageAvails)

admin.site.register(Appointment, ManageAppointment)

admin.site.register(Client, ManageClient)

admin.site.register(Schedule, ManageStaffSchedule)
