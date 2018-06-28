from django.db import models
from orims.models import Staff


# Appointment model
class Appointment(models.Model):
    """"Creates and associates with a database relation that store data about official - client appointment"""
    # Appointment primary key
    appointment_id = models.CharField(primary_key=True,max_length = 30)
    # Setting foreign key
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    # appointment attributes
    placement_time = models.DateTimeField()
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    reason = models.TextField(max_length=512)
    appointment_mode_choices = (
        ('pend', 'Pending'),
        ('canc', 'Canceled'),
        ('fwd', 'Forwarded'),
        ('conf', 'Confirmed'),
        ('setd', 'Settled'),
        ('non', 'None')
    )

    # Creating mode choices for appointment
    appointment_mode = models.CharField(
        max_length=15,
        choices=appointment_mode_choices,
        default='non',
    )

    # Defining a display string for each instance
    def __str__(self):
        return self.appointment_id
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Appointment"
    # End class Meta
# End class Appointment


# Client model
class Client(models.Model):
    """"Creates and associates with a database relation that store data about a client from public"""
    # Setting foreign key
    appointment_id = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    # client attributes
    client_first_name = models.CharField(max_length=15)
    client_last_name = models.CharField(max_length=15)
    client_contact = models.CharField(max_length=15)
    client_location_district = models.CharField(max_length=15)
    client_location_town = models.CharField(max_length=15)

    # Defining a display string for each instance
    def __str__(self):
        return "%s %s", self.client_first_name, self.client_last_name
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Client"
    # End class Meta
# End class Client


# Model Staff Schedule
class Schedule(models.Model):
    """"Creates and associates with a database relation that store data about official monthly schedule"""
    # Setting foreign key
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    # schedule attributes
    sch_date = models.DateField('Date when Schedule is made',max_length=3)
    start_time = models.TimeField()
    end_time = models.TimeField()
    # If reason is Appointment, default sch_reason is "Appointment.
    appointment_id = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    # If any other reason".
    sch_reason = models.TextField(max_length=512)

    # Defining a display string for each instance
    def __str__(self):
        sch = "Scheduled on %s. Schedule duration [from %s to %s]", self.sch_date, self.start_time, self.end_time
        return sch
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Schedule"
    # End class Meta
# End class Schedule
