from django import forms
from django.contrib.auth.hashers import make_password
from user_registration.models import PatientProfile, EmployeeProfile, BillingReminder


class PatientRegistrationForm(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email')
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self):
        patient_profile = PatientProfile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            username=self.cleaned_data['username'],
            password=make_password(self.cleaned_data['password']),
        )
        patient_profile.save()


class EmployeeRegistrationForm(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email')
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self):
        employee_profile = EmployeeProfile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            username=self.cleaned_data['username'],
            password=make_password(self.cleaned_data['password']),
        )
        employee_profile.save()


class PatientLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = '__all__'


class EmployeeLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = '__all__'


class BillingReminderForm(forms.ModelForm):
    class Meta:
        model = BillingReminder
        fields = ['message', 'send_datetime', 'user']
