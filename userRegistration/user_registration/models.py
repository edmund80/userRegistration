from django.db import models
from django.contrib.auth.models import User


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    first_name = models.CharField(null=True)
    last_name = models.CharField(null=True)
    address = models.CharField(null=True)
    city = models.CharField(null=True)
    state = models.CharField(null=True)
    zip = models.CharField(null=True)
    phone = models.CharField(null=True)
    email = models.EmailField(null=True)
    medications = models.CharField(null=True)
    diagnosis = models.CharField(null=True)
    insurance_card = models.ImageField(upload_to='images', null=True)
    id_card = models.ImageField(upload_to='images', null=True)
    next_of_kin_name = models.CharField(null=True)
    next_of_kin_number = models.CharField(null=True)
    text_billing_reminder = models.BooleanField(null=True)
    email_billing_reminder = models.BooleanField(null=True)
    text_appointment_reminder = models.BooleanField(null=True)
    email_appointment_reminder = models.BooleanField(null=True)


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', null=True)
    first_name = models.CharField(null=True)
    last_name = models.CharField(null=True)
    address = models.CharField(null=True)
    city = models.CharField(null=True)
    state = models.CharField(null=True)
    zip = models.CharField(null=True)
    phone = models.CharField(null=True)
    email = models.EmailField(null=True)
    supervisor = models.BooleanField(null=True)


class BillingReminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    send_datetime = models.DateTimeField()
