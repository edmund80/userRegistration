from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import ListView
from rest_framework import generics
from .serializers import PatientProfileSerializer, EmployeeProfileSerializer
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PatientRegistrationForm, EmployeeRegistrationForm, PatientLoginForm, EmployeeLoginForm, \
    PatientProfileForm, EmployeeProfileForm, BillingReminderForm, AppointmentReminderForm
from .models import PatientProfile, EmployeeProfile, BillingReminder, AppointmentReminder, Appointment, BillingStatement
from django.contrib.auth.models import User
from datetime import datetime
from django.core.mail import send_mail


# Create your views here.
def home(request):
    return render(request, 'index.html')


class PatientProfileListCreateView(generics.ListCreateAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer


class PatientProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer


class EmployeeProfileListCreateView(generics.ListCreateAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer


class EmployeeProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer


def patient_registration_view(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            patient_profile = PatientProfile.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            return redirect('patient_login')
    else:
        form = PatientRegistrationForm()

    return render(request, 'patient_registration.html', {'form': form})


def employee_registration_view(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            employee_profile = EmployeeProfile.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            return redirect('employee_login')
    else:
        form = EmployeeRegistrationForm()

    return render(request, 'employee_registration.html', {'form': form})


def patient_login(request):
    if request.method == 'POST':
        form = PatientLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('patient_update_profile',
                                pk=user.patientprofile.pk)
            else:
                return render(request, 'patient_login.html', {'form': form, 'error_message': 'Invalid login'})
    else:
        form = PatientLoginForm()

    return render(request, 'patient_login.html', {'form': form})


def employee_login(request):
    if request.method == 'POST':
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('employee_update_profile',
                                pk=user.employeeprofile.pk)  # Redirect to employee_update_profile
            else:
                return render(request, 'employee_login.html', {'form': form, 'error_message': 'Invalid login'})
    else:
        form = EmployeeLoginForm()

    return render(request, 'employee_login.html', {'form': form})


def patient_landing(request):
    patient_profile = PatientProfile.objects.get(user=request.user)
    return render(request, 'patient_landing_page.html', {'patient_profile': patient_profile})


def employee_landing(request):
    employee_profile = EmployeeProfile.objects.get(user=request.user)
    return render(request, 'employee_landing_page.html', {'employee_profile': employee_profile})


def patient_update_profile(request, pk):
    patient = PatientProfile.objects.get(pk=pk)
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
        else:
            form = PatientProfileForm(instance=patient)

    return redirect('patient_landing')


# Edit employee profile view
def employee_update_profile(request, pk):
    employee = EmployeeProfile.objects.get(pk=pk)
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
    else:
        form = EmployeeProfileForm(instance=employee)

    return redirect('employee_landing')


def employee_profile(request, pk):
    employee_profile = get_object_or_404(EmployeeProfile, pk=pk)
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, request.FILES, instance=employee_profile)
        if form.is_valid():
            form.save()
        return redirect('employee_landing')
    else:
        form = EmployeeProfileForm(instance=employee_profile)
    return render(request, 'employee_profile.html', {'form': form})


def patient_profile(request, pk):
    patient_profile = get_object_or_404(PatientProfile, pk=pk)
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, request.FILES, instance=patient_profile)
        if form.is_valid():
            form.save()
        return redirect('patient_landing')
    else:
        form = PatientProfileForm(instance=patient_profile)
    return render(request, 'patient_profile.html', {'form': form})


def appointment_list(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'appointment_list.html', {'appointments': appointments})


def confirm_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.confirmed = True
    appointment.save()
    return redirect('appointment_list')


def send_billing_reminders(request):
    now = datetime.now()
    reminders = BillingReminder.objects.filter(send_datetime__lte=now)
    for reminder in reminders:
        if reminder.user.email_billing_reminder:
            subject = "Billing Reminder"
            html_message = render_to_string('billing_reminder_email_template.html', {'reminder': reminder})
            plain_message = strip_tags(html_message)
            from_email = 'your-email@example.com'
            to_email = reminder.user.email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
            print('Billing Reminder Sent')
        else:
            print('User has not opted in for billing reminders.')
    reminders.delete()
    return HttpResponse('Billing reminders sent successfully')


def send_appointment_reminders(request):
    now = datetime.now()
    reminders = AppointmentReminder.objects.filter(send_datetime__lte=now)
    for reminder in reminders:
        if reminder.user.email_appointment_reminder:
            subject = "Appointment Reminder"
            html_message = render_to_string('appointment_reminder_email_template.html', {'reminder': reminder})
            plain_message = strip_tags(html_message)
            from_email = 'your-email@example.com'
            to_email = reminder.user.email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
            print('Appointment Reminder Sent')
        else:
            print('User has not opted in for appointment reminders.')
    reminders.delete()
    return HttpResponse('Appointment reminders sent successfully')


def create_billing_reminder(request):
    if request.method == 'POST':
        form = BillingReminderForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            # Trigger the sending of billing reminders
            send_billing_reminders(request)
            print('Billing Reminder Sent')
            # Reset the form
            form = BillingReminderForm()
        return redirect('billing_reminders')
    else:
        form = BillingReminderForm()
    return render(request, 'create_billing_reminder.html', {'form': form})


def create_appointment_reminder(request):
    if request.method == 'POST':
        form = AppointmentReminderForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            # Trigger the sending of appointment reminders
            send_appointment_reminders(request)
            print('Appointment Reminder Sent')
            # Reset the form
        form = AppointmentReminderForm()
        return redirect('appointment_reminders')
    else:
        form = AppointmentReminderForm()
    return render(request, 'create_appointment_reminder.html', {'form': form})


class BillingStatementListView(LoginRequiredMixin, ListView):
    model = BillingStatement
    template_name = 'billing_statement_list.html'
    context_object_name = 'billing_statements'

    def get_queryset(self):
        # Only show statements for logged-in user.
        return BillingStatement.objects.filter(user=self.request.user)
