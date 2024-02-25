from rest_framework import serializers
from .models import PatientProfile, EmployeeProfile, BillingReminder
class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = '__all__'


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = '__all__'


class BillingReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingReminder
        fields = '__all__'
