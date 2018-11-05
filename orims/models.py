from django.db import models
from systemAdmin.models import SystemAdmin
from orims.custom import RandomFileName
import uuid

# Added imports
from django.utils import timezone

# Model Class for service Unit
class ServiceUnit(models.Model):
    """"
    Creates and associates with a database relation that store data about a service unit / facility.
    i.e. [Ministry, Organisation, firm, etc.]
    """
    # Setting foreign key
    system_admin_id = models.ForeignKey(SystemAdmin, on_delete=models.CASCADE,verbose_name='System Administrator')
    # Setting custom Primary key
    unit_id = models.AutoField(primary_key=True, verbose_name='Service Unit ID')
    unit_name = models.CharField('Service Unit name', max_length=500)
    # Defining possible service unit types to form a lookup.
    unit_choice = (
        ('select', '--Select Category--'),
        ('Association', 'Association'),
        ('Business Firm', 'Business Firm'),
        ('Clinic', 'Clinic'),
        ('Club', 'Club'),
        ('Cooperative Society', 'Cooperative Society'),
        ('Drug Shop', 'Drug Shop'),
        ('Financial Institution', 'Financial Institution'),
        ('Group', 'Group'),
        ('Health Center', 'Health Center'),
        ('Hospital', 'Hospital'),
        ('Institute', 'Institute'),
        ('Institution', 'Institution'),
        ('Law Firm', 'Law Firm'),
        ('Media House', 'Media House'),
        ('Ministry', 'Ministry'),
        ('Organisation', 'Organisation'),
        ('Pharmacy', 'Pharmacy'),
        ('School', 'School'),
        ('Society', 'Society'),
        ('University', 'University'),
        ('Other', 'Others'),
    )
    # Creating a choice of service units
    unit_type = models.CharField(
        'Service Unit Category',
        max_length=30,
        choices=unit_choice,
        default='select',
    )
    unit_description = models.TextField(max_length=1024)
    unit_logo = models.FileField(upload_to=RandomFileName('photos/uploads/ServiceUnit/logos'),
                                 max_length=2000,null = True,blank = True)
    unit_featured_image = models.FileField(upload_to=RandomFileName('photos/uploads/ServiceUnit/featured_images'),
                                           max_length=2000,null = True,blank = True)
    unit_cover_photo = models.FileField(upload_to=RandomFileName('photos/uploads/ServiceUnit/cover_photos'),
                                        max_length=2000,null = True,blank = True)
    true = auto_now = True
    registration_date = models.DateTimeField(default=timezone.now)

    # Defining what to be returned for each instance
    def __str__(self):
        # ret_str = "%s (%d)", self.unit_name, self.unit_id
        ret_str = str(self.unit_name) + ' ( Unit Id :  ' + str(self.unit_id) + ' )'
        return str(ret_str)
    # End of function __str__(self)

    # Enforcing custom table name
    class Meta:
        db_table = "ServiceUnit"
        ordering = ['-registration_date']
    # End class Meta
# End class ServiceUnit


# Model for service unit branches
class Branch(models.Model):
    """"
    Creates and associates with a database relation that store data about a branch of an organization
    """
    # Setting custom Primary key
    branch_id = models.AutoField(primary_key=True)
    # Setting foreign key
    unit_id = models.ForeignKey(ServiceUnit, on_delete=models.CASCADE, verbose_name='Service unit')
    branch_name = models.CharField(max_length=200)
    # Defining possible branch levels to form a lookup.
    branch_level_choice = (
        ('main', 'Main Branch'),
        ('other', 'Other Branch')
    )
    # Creating a choice of service units Branch levels
    branch_level = models.CharField(
        max_length=15,
        choices=branch_level_choice,
        default='other',
    )
    registration_date = models.DateTimeField(default=timezone.now)

    safe_id = ''

    def set_safe_id(self):
        self.safe_id = self.unit_id

    # Defining a display string for each instance
    def __str__(self):
        return str(self.unit_id) + ' - ' + str(self.branch_name) + ' Branch ( ID: ' + str(self.branch_id) + ' )'
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Branch"
        verbose_name_plural = "Branches"
    # End class Meta
# End class Branch


# Model for branch location
class Location(models.Model):
    """"Creates and associates with a database relation that store data about a branch location information"""
    # Setting foreign key
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Branch')
    # Location attributes
    district = models.CharField(max_length=50)
    county = models.CharField(max_length=50, null=True, blank=True)
    sub_county = models.CharField(max_length=50, null=True, blank=True)
    parish = models.CharField(max_length=50, null=True, blank=True)
    town = models.CharField(max_length=50)
    zone = models.CharField(max_length=50, null=True, blank=True)
    plot_no = models.CharField(max_length=50, null=True, blank=True)
    building = models.CharField(max_length=50, null=True, blank=True)
    unique_direction = models.CharField(max_length=250, null=True, blank=True)

    # Defining a display string for each instance
    def __str__(self):
        return str(self.branch_id) + ',  ' + str(self.town) + ' - ' + str(self.district)
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Location"
    # End class Meta
# End class Location


# Model for branch Contact information
class Contact(models.Model):
    """"
    Creates and associates with a database relation that store data about a branch contacts information
    """
    # Setting foreign key
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE,verbose_name='Branch')
    # Contact attributes
    mobile_number = models.CharField(max_length=15)
    office_number = models.CharField(max_length=15, blank=True)
    fax_number = models.CharField(max_length=15, blank=True)
    email_address = models.EmailField(max_length=250, null=True, blank=True)

    # Defining a display string for each instance
    def __str__(self):
        return str(self.branch_id)
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Contact"
    # End class Meta
# End class Contact


# Model for branch department
class Department(models.Model):
    """"
    Creates and associates with a database relation that store data about a department.
    """
    # Department primary key
    department_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    # models.CharField(primary_key=True,max_length=512)
    # Setting foreign key
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Branch')
    # Department attributes
    department_name = models.CharField(max_length=250)
    department_description = models.TextField('Description', max_length=1024)
    registration_date = models.DateTimeField(default=timezone.now)

    # Defining a display string for each instance
    def __str__(self):
        return str(self.branch_id) + ' - ' + str(self.department_name) + ' Department'
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Department"
    # End class Meta
# End class Department


# Model for office under department of a branch
class Office(models.Model):
    """"
    Creates and associates with a database relation that store data about an office
    """
    # Office primary key
    office_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    # office_id = models.CharField(primary_key=True, max_length=512)
    # Setting foreign key
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Department')
    # Department attributes
    office_name = models.CharField(max_length=50)
    office_description = models.TextField(max_length=1024)
    office_working_time_choice = (
        ('Standard', 'Standard Working Time and Days'),
        ('Custom', 'Set Custom Working Time for office'),
    )
    office_working_time = models.CharField(
        max_length=30,
        choices=office_working_time_choice,
        default='Standard',
    )
    registration_date = models.DateTimeField(default=timezone.now)

    # Defining a display string for each instance
    def __str__(self):
        return str(self.department_id) + ' - Office of ' + str(self.office_name)
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Office"
    # End class Meta
# End class Office


# Model for Custom working time for an office
class WorkingTime(models.Model):
    """"
    Creates and associates with a database relation that store data about an office working hours
    """
    # Setting foreign key
    office_id = models.ForeignKey(Office, on_delete=models.CASCADE, verbose_name='Office')
    # working time attributes
    week_day_choices = (
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
        ('non', 'Select Week Day'),
    )
    week_day = models.CharField(
        max_length=3,
        choices=week_day_choices,
        default='non',
    )
    work_start_time = models.TimeField(default='08:00:00')
    work_end_time = models.TimeField(default='17:00:00')

    # Defining a display string for each instance
    def __str__(self):
        return str(self.office_id) + ' - ' + str(self.week_day) + ' From ' + str(self.work_start_time) + ' To ' + str(self.work_end_time)
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "WorkingTime"
    # End class Meta
# End class WorkingTime


# Staff model
class Staff(models.Model):
    """"Creates and associates with a database relation that store data about a staff member"""
    # staff primary key
    staff_id = models.CharField(primary_key=True, max_length=200)
    # Setting foreign key
    office_id = models.ForeignKey(Office, on_delete=models.CASCADE, verbose_name='Office')
    # staff attributes
    staff_first_name = models.CharField('First Name', max_length=30)
    staff_last_name = models.CharField('Last Name', max_length=30)
    staff_profile_photo = models.CharField('Profile Photo', max_length=512, blank=True, null=True)
    staff_designation_choices = (
        # ('system_admin', 'System administrator'),
        ('Official', 'Official'),
        ('receptionist', 'Receptionist'),
        ('select', '---Select Staff Designation---')
    )
    # Creating choices for staff
    staff_designation = models.CharField(
        'Designation',
        max_length=15,
        choices=staff_designation_choices,
        default='select',
    )
    about_staff = models.TextField(max_length=512, blank=True, null=True)
    registration_date = models.DateTimeField(default=timezone.now)

    # Defining a display string for each instance
    def __str__(self):
        return str(self.staff_first_name) + ' ' + str(self.staff_last_name) + ' [ ID: ' + str(self.staff_id) + ' ]'
    # End function __str__()

# End class Staff
