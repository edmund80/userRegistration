from django.contrib import admin
from django.contrib import admin
from .models import PatientProfile, EmployeeProfile, BillingReminder, AppointmentReminder, Appointment

# Register your models here.
admin.site.register(PatientProfile)
admin.site.register(EmployeeProfile)
admin.site.register(BillingReminder)
admin.site.register(AppointmentReminder)
admin.site.register(Appointment)
# Register your models here.
