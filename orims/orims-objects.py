#ORIMS OBJECTS
from django.urls import path
from . import models

class system_admin():
    admin_id = ""
    office_id = ""
    first_name = ""
    last_name = ""
    user_name = ""
    profile_photo = ""
    profile = ""

    def __init__(self,adm_id):
        admin_id = adm_id

    def register_admin(self):
        #staff_registration(admin_id)

        #ASSUMPTION
        stf = staff(staff_id = "123",staff_first_name = "SSENENGO")
        stf

    def set_admin_data(self):
        pass
        

xx = system_admin("")
print(xx.register_admin())
