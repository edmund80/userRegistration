from django.db import models
from django.contrib.auth.models import User


class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_administrator = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zip = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    medications = models.CharField(max_length=255, null=True)
    diagnosis = models.CharField(max_length=255, null=True)
    insurance_card = models.ImageField(upload_to='images', null=True)
    id_card = models.ImageField(upload_to='images', null=True)
    next_of_kin_name = models.CharField(max_length=100, null=True)
    next_of_kin_number = models.CharField(max_length=20, null=True)
    text_billing_reminder = models.BooleanField(default=False, null=True)
    email_billing_reminder = models.BooleanField(default=False, null=True)
    text_appointment_reminder = models.BooleanField(default=False, null=True)
    email_appointment_reminder = models.BooleanField(default=False, null=True)


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zip = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    administrator = models.OneToOneField(Administrator, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    confirmed = models.BooleanField(default=False)


class BillingStatement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    billing_period = models.CharField(max_length=50)
    statement_date = models.DateField()
    due_date = models.DateField()
    total_charges = models.DecimalField(max_digits=10, decimal_places=2)
    payments_received = models.DecimalField(max_digits=10, decimal_places=2)
    outstanding_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Billing Statement for {self.user.username}"


class BillingReminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    send_datetime = models.DateTimeField()


class AppointmentReminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    send_datetime = models.DateTimeField()
