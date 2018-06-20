from django.db import models

# Added imports
#from django.utils import timezone

class service_unit(models.Model):
    'This is the common base class (model) for a particular service unit / facility. i.e. [Ministry, Organisation, firm, etc.]'
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
    'This is the common base class (model) define storage relation of data for each branch of a particular service unit.'
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
    'This is the common base class (model) that depicts locations for each branch of a particular service unit'
    # Setting foreign key
    branch_id = models.ForeignKey(branch, on_delete=models.CASCADE) 
    #Location attributes
    district = models.CharField(max_length=15)
    county = models.CharField(max_length=15,null = True,blank = True)
    sub_county = models.CharField(max_length=15,null = True,blank = True)
    parish = models.CharField(max_length=15,null = True,blank = True)
    town = models.CharField(max_length=15)
    zone = models.CharField(max_length=15,null = True,blank = True)
    unique_direction = models.CharField(max_length=15,null = True,blank = True)
    #Defining a display string for each instance
    def __str__(self):
        return self.branch_name
    #Enforcing custom table name
    class Meta:
        db_table = "location"



# Model for branch Contact information
class contact(models.Model):
    'This is the common base class (model) that illustrate storage of contact information for each branch of a particular service units.'
    # Setting foreign key
    branch_id = models.ForeignKey(branch, on_delete=models.CASCADE)
    #Contact attributes
    mobile_number = models.CharField(max_length=15)
    office_number = models.CharField(max_length=15,null = True,blank = True)
    fax_number = models.CharField(max_length=15,null = True,blank = True)
    email_address = models.CharField(max_length=15,null = True,blank = True)
    #Defining a display string for each instance
    def __str__(self):
        return self.branch_name
    #Enforcing custom table name
    class Meta:
        db_table = "contact"



# Model for branch department
class department(models.Model):
    'This is the common base class (model) that illustrate departiment information for each department under a branch of a particular service unit.'
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



# Model for office under department of a branch
class office(models.Model):
    'This is the common base class (model) that illustrate office information for each office under department under a branch of a particular service unit.'
    #Office primary key
    office_id = models.CharField(primary_key=True, max_length = 30)
    # Setting foreign key
    department_id = models.ForeignKey(department, on_delete=models.CASCADE)
    #Department attributes
    office_name = models.CharField(max_length=50)
    office_description = models.TextField(max_length=1024)
    #Defining a display string for each instance
    def __str__(self):
        return self.office_name
    #Enforcing custom table name
    class Meta:
        db_table = "office"



# Staff model
class staff(models.Model):
    'This is the common base class (model) that illustrate details of a staff member departiment information for each department under a branch of a particular service unit.'
    #staff primary key
    staff_id = models.CharField(primary_key=True,max_length = 30)
    # Setting foreign key
    office_id = models.ForeignKey(office, on_delete=models.CASCADE)
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
    'This is the common base class (model) that illustrate details of each system user'
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
    'This is the common base class (model) that illustrate details of each system administrator'
    # Setting foreign key
    staff_id = models.ForeignKey(staff, on_delete=models.CASCADE)
    #User attributes
    branch_id = models.ForeignKey(branch, on_delete=models.CASCADE)
    admin_level_choices = (
        ('unit-admin', 'Main System administrator'),
        ('branch-admin', 'Branch system administrator'),
        ('select','Select administrator level')
    )
    #Creating choices for staff
    admin_level = models.CharField(
        max_length=30,
        choices=admin_level_choices,
        default='select',
    )
    #Defining a display string for each instance
    def __str__(self):
        return self.staff_id
    #Enforcing custom table name
    class Meta:
        db_table = "system_admin"



# Avails model
class avails(models.Model):
    'This is the common base class (model) that defines a relation to store data about the availing relationship'
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
    'This is the common base class (model) that defines a relation to store data about each appointment'
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
        ('pend', 'Pending'),
        ('canc', 'Canceled'),
        ('setd', 'Settled'),
        ('slct','Select Appointment Mode')
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
    'This is the common base class (model) that defines a relation to store data about a client each time of an appointment instance.'
    # Setting foreign key
    appointment_id = models.ForeignKey(appointment, on_delete=models.CASCADE)
    #client attributes
    client_first_name = models.CharField(max_length=15)
    client_last_name = models.CharField(max_length=15)
    client_contact = models.CharField(max_length=15)
    client_location_district = models.CharField(max_length=15)
    client_location_town = models.CharField(max_length=15)
    #Defining a display string for each instance
    def __str__(self):
        return self.client_first_name + self.client_last_name
    #Enforcing custom table name
    class Meta:
        db_table = "client"
