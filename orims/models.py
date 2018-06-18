from django.db import models

# Added imports
from django.utils import timezone

# CREATION OF ORIMS DATABASE MODELS.

# Model for service unit object
class service_unit(models.Model):
    'This is the common base class (model) for all service facility units. i.e. [Ministries, Organisations, firms, etc.]'
    # Setting custom Primary key
    unit_id = models.AutoField(primary_key=True)
    unit_name = models.CharField(max_length=30)
    
    #Defining possible service unit types to form a lookup.
    ministry = 'min'
    organization = 'org'
    firm = 'firm'
    other = 'other'
    unit_choice = (
        ('select','Select Type of service unit'),
    	(ministry, 'Ministry'),
    	(organization,'Organization'),
    	(firm,'Firm'),
    	(other,'Others')
    )

    #Creating a choice of service units
    unit_type = models.CharField(
    	max_length=15,
    	choices=unit_choice,
        default='select',
    )

    unit_description = models.TextField(max_length=1024)
    unit_logo = models.CharField(max_length=500)
    unit_featured_image = models.CharField(max_length=500)
    unit_cover_photo = models.CharField(max_length=500)

    #Defining what to be returned for each instance
    def __str__(self):
        return self.unit_name

    #Enforcing custom table name
    class Meta:
        db_table = "service_unit"



# Model for service unit branches
class branch(models.Model):
    'This is the common base class (model) for all service units branches.'

    # Setting custom Primary key
    branch_id = models.AutoField(primary_key=True)

    # Setting foreign key
    unit_id = models.ForeignKey(service_unit, on_delete=models.CASCADE)

    branch_name = models.CharField(max_length=30)
    
    #Defining possible branch levels to form a lookup.
    
    branch_level_choice = (
        ('main', 'Main Branch'),
        ('other','Other Branch')
    )

    #Creating a choice of service units Branch levels
    branch_level = models.CharField(
        max_length=15,
        choices=branch_level_choice,
        default='other',
    )

    registration_date = models.DateTimeField()


    #Defining a display string for each instance
    def __str__(self):
        return self.branch_name

    #Enforcing custom table name
    class Meta:
        db_table = "branch"


# Model for branch location
class location(models.Model):
    'This is the common base class (model) for all branch locations'

    # Setting foreign key
    branch_id = models.ForeignKey(branch, on_delete=models.CASCADE)
 
    #Location attributes
    district = models.CharField(max_length=15)
    county = models.CharField(max_length=15)
    sub_county = models.CharField(max_length=15)
    parish = models.CharField(max_length=15)
    town = models.CharField(max_length=15)
    zone = models.CharField(max_length=15)
    unique_direction = models.CharField(max_length=15)

    #Defining a display string for each instance
    def __str__(self):
        return self.branch_name

    #Enforcing custom table name
    class Meta:
        db_table = "location"


# Model for branch Contact information
class contact(models.Model):

    # Setting foreign key
    branch_id = models.ForeignKey(branch, on_delete=models.CASCADE)
 
    #Contact attributes
    mobile_number = models.CharField(max_length=15)
    office_number = models.CharField(max_length=15)
    fax_number = models.CharField(max_length=15)
    email_address = models.CharField(max_length=15)

    #Defining a display string for each instance
    def __str__(self):
        return self.branch_name

    #Enforcing custom table name
    class Meta:
        db_table = "contact"

# Model for branch Contact information
class department(models.Model):

    #Department primary key
    department_id = models.CharField(primary_key=True, max_length = 30)
    # Setting foreign key
    branch_id = models.ForeignKey(branch, on_delete=models.CASCADE)
 
    #Department attributes
    department_name = models.CharField(max_length=50)
    department_description = models.TextField(max_length=1024)

    #Defining a display string for each instance
    def __str__(self):
        return self.department_name

    #Enforcing custom table name
    class Meta:
        db_table = "department"


# Staff model
class staff(models.Model):

    #staff primary key
    staff_id = models.CharField(primary_key=True,max_length = 30)
    # Setting foreign key
    department_id = models.ForeignKey(department, on_delete=models.CASCADE)
 
    #staff attributes
    staff_first_name = models.CharField(max_length=15)
    staff_last_name = models.CharField(max_length=15)
    staff_profile_photo = models.CharField(max_length=512)

    staff_designation_choices = (
        ('system_admin', 'System administrator'),
        ('Official', 'Official'),
        ('receptionist', 'Receptionist'),
        ('select','Select Staff Designation')
    )

    #Creating choices for staff
    staff_designation = models.CharField(
        max_length=15,
        choices=staff_designation_choices,
        default='select',
    )
    
    about_staff = models.TextField(max_length=512)

    #Defining a display string for each instance
    def __str__(self):
        return self.staff_first_name + self.staff_last_name

    #Enforcing custom table name
    class Meta:
        db_table = "staff"



# user model
class user(models.Model):

    # Setting foreign key
    staff_id = models.ForeignKey(staff, on_delete=models.CASCADE)
 
    #User attributes
    user_name = models.CharField(unique=True,max_length=15)
    user_password = models.CharField(max_length=100)


    #Defining a display string for each instance
    def __str__(self):
        pass

    #Enforcing custom table name
    class Meta:
        db_table = "user"


# System administrator model
class system_admin(models.Model):

    # Setting foreign key
    staff_id = models.ForeignKey(staff, on_delete=models.CASCADE)
 
    #User attributes
    branch_id = models.ForeignKey(branch, on_delete=models.CASCADE)


    #Defining a display string for each instance
    def __str__(self):
        return self.staff_id

    #Enforcing custom table name
    class Meta:
        db_table = "system_admin"



# Avails model
class avails(models.Model):

    # Setting foreign key
    availer = models.CharField(max_length = 15)
    availed = models.ForeignKey(staff, on_delete=models.CASCADE)
    session_start = models.DateTimeField()
    session_stop = models.DateTimeField()

    #Defining a display string for each instance
    def __str__(self):
        pass

    #Enforcing custom table name
    class Meta:
        db_table = "avails"




# Appointment model
class appointment(models.Model):
    #Appointment primary key
    appointment_id = models.CharField(primary_key=True,max_length = 30)
 
    # Setting foreign key
    staff_id = models.ForeignKey(staff, on_delete=models.CASCADE)
 
    #appointment attributes
    placement_time = models.DateTimeField()
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    reason = models.TextField(max_length=512)

    appointment_mode_choices = (
        ('pending', 'Pending'),
        ('canceled', 'Canceled'),
        ('settled', 'Settled'),
        ('select','Select Appointment Mode')
    )

    #Creating mode choices for appointment
    appointment_mode = models.CharField(
        max_length=15,
        choices=appointment_mode_choices,
        default='select',
    )

   
    #Defining a display string for each instance
    def __str__(self):
        return self.appointment_id

    #Enforcing custom table name
    class Meta:
        db_table = "appointment"



# Client model
class client(models.Model):

    # Setting foreign key
    appointment_id = models.ForeignKey(appointment, on_delete=models.CASCADE)
 
    #client attributes
    client_first_name = models.CharField(max_length=15)
    client_last_name = models.CharField(max_length=15)
    client_contact = models.CharField(max_length=15)
    location_district = models.CharField(max_length=15)
    location_town = models.CharField(max_length=15)

    #Defining a display string for each instance
    def __str__(self):
        return self.client_first_name + self.client_last_name

    #Enforcing custom table name
    class Meta:
        db_table = "client"



