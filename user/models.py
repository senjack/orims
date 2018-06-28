from django.db import models
from  orims.models import Staff

# user model
class User(models.Model):
    """"
    Creates and associates with a database relation that store data about a system user
    """
    # Setting foreign key
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    # User attributes
    user_name = models.CharField(unique=True, max_length=15)
    user_password = models.CharField(max_length=50)

    # Defining a display string for each instance
    def __str__(self):
        return '%(%s)', self.user_name, self.staff_id
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "User"
    # End class Meta
# End class User
