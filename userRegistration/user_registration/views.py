from rest_framework import generics
from .serializers import PatientProfileSerializer, EmployeeProfileSerializer
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PatientRegistrationForm, EmployeeRegistrationForm, PatientLoginForm, EmployeeLoginForm, \
    PatientProfileForm, EmployeeProfileForm, BillingReminderForm
from .models import PatientProfile, EmployeeProfile, BillingReminder
from django.contrib.auth.models import User
from django.conf import settings
from twilio.rest import Client
from datetime import datetime
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path


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


def send_billing_reminders():
    now = datetime.now()
    reminders = BillingReminder.objects.filter(send_datetime__lte=now)
    for reminder in reminders:
        # Check for the user's preference
        if reminder.user.email_billing_reminder or reminder.user.text_billing_reminder:
            # Determine message type
            message_type = 'email' if reminder.user.email_billing_reminder else 'text'

            # Send Email Or Text Reminder
            try:
                if message_type == 'email':
                    # Send reminder via email
                    html = Template(Path('index.html').read_text())
                    email = EmailMessage()
                    email['from'] = 'Squad 2 Healthcare System'
                    email['to'] = reminder.user.email
                    email['subject'] = reminder.message


                    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                        email_address = ''
                        email_password = ''
                        smtp.ehlo()
                        smtp.starttls()
                        smtp.login(email_address, email_password)
                        smtp.send_message(email)
                        print('Billing Reminder Sent')
                elif message_type == 'text':
                    # Send reminder via text (Twilio)
                    client = Client('', '')
                    message = client.messages.create(
                        body=reminder.message,
                        from_='',
                        to=reminder.user.phone
                    )
                    # Log the SMS sent successfully message
                    print(f'SMS sent successfully. SID: {message.sid}')

            except Exception as e:
                print(f'Error sending reminder: {e}')

        else:
            print('User has not opted in for reminders.')

    # Delete the reminders after sending
    reminders.delete()


def create_billing_reminder(request):
    if request.method == 'POST':
        form = BillingReminderForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            # Trigger the sending of billing reminders
            send_billing_reminders()
            print('Billing Reminder Sent')
            # Reset the form
            form = BillingReminderForm()
            return redirect('billing_reminders')  # Redirect to a success page or another view
    else:
        form = BillingReminderForm()
    return render(request, 'create_billing_reminder.html', {'form': form})
