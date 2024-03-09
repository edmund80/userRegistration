from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from .models import PatientProfile, EmployeeProfile, Administrator, Appointment, BillingReminder, AppointmentReminder
from django.contrib.auth.models import User


class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', email='test@example.com', password='test_password'
        )

    def test_administrator_model(self):
        """Test the Administrator model."""
        admin = Administrator.objects.create(user=self.user, is_administrator=True)
        self.assertEqual(admin.user.username, 'test_user')
        self.assertTrue(admin.is_administrator)

    def test_patient_profile_model(self):
        """Test the PatientProfile model."""
        patient_profile = PatientProfile.objects.create(
            user=self.user,
            image='img.png',
            first_name='John',
            last_name='Doe',
            address='123 Main St',
            city='Anytown',
            state='NY',
            zip='12345',
            phone='555-1234',
            email='john.doe@example.com',
            medications='Med1, Med2',
            diagnosis='Diagnosis',
            next_of_kin_name='Jane Doe',
            next_of_kin_number='555-5678',
            text_billing_reminder=True,
            email_billing_reminder=False,
            text_appointment_reminder=True,
            email_appointment_reminder=False
        )
        self.assertEqual(patient_profile.user.username, 'test_user')
        self.assertEqual(patient_profile.first_name, 'John')
        # Add more assertions for other fields

    def test_employee_profile_model(self):
        """Test the EmployeeProfile model."""
        employee_profile = EmployeeProfile.objects.create(
            user=self.user,
            image='img.png',
            first_name='Jane',
            last_name='Smith',
            address='456 Elm St',
            city='Othertown',
            state='CA',
            zip='54321',
            phone='555-4321',
            email='jane.smith@example.com'
        )
        self.assertEqual(employee_profile.user.username, 'test_user')
        self.assertEqual(employee_profile.first_name, 'Jane')
        # Add more assertions for other fields

    def test_appointment_model(self):
        """Test the Appointment model."""
        appointment = Appointment.objects.create(
            patient=self.user,
            date='2024-03-07',
            time='08:00:00',
            confirmed=False
        )
        self.assertEqual(appointment.patient.username, 'test_user')
        self.assertEqual(str(appointment.date), '2024-03-07')
        self.assertEqual(str(appointment.time), '08:00:00')
        self.assertFalse(appointment.confirmed)

    def test_billing_reminder_model(self):
        """Test the BillingReminder model."""
        billing_reminder = BillingReminder.objects.create(
            user=self.user,
            message='Billing Reminder Message',
            send_datetime='2024-03-07 12:00:00'
        )
        self.assertEqual(billing_reminder.user.username, 'test_user')
        self.assertEqual(billing_reminder.message, 'Billing Reminder Message')
        self.assertEqual(str(billing_reminder.send_datetime), '2024-03-07 12:00:00')

    def test_appointment_reminder_model(self):
        """Test the AppointmentReminder model."""
        appointment_reminder = AppointmentReminder.objects.create(
            user=self.user,
            message='Appointment Reminder Message',
            send_datetime='2024-03-07 12:00:00'
        )
        self.assertEqual(appointment_reminder.user.username, 'test_user')
        self.assertEqual(appointment_reminder.message, 'Appointment Reminder Message')
        self.assertEqual(str(appointment_reminder.send_datetime), '2024-03-07 12:00:00')


