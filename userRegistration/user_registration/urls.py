from django.urls import path
from .views import home, PatientProfileListCreateView, PatientProfileRetrieveUpdateDestroyView, \
    EmployeeProfileListCreateView, \
    EmployeeProfileRetrieveUpdateDestroyView, patient_landing, patient_registration_view, employee_update_profile, \
    employee_registration_view, \
    patient_update_profile, employee_login, patient_login, employee_landing, employee_profile, patient_profile, \
    send_billing_reminders, create_billing_reminder, send_appointment_reminders, create_appointment_reminder, \
    appointment_list, confirm_appointment

urlpatterns = [
    path('home/', home, name='home'),
    path('api/user_registration_patientprofile/', PatientProfileListCreateView.as_view(), name='patientprofile-list-create'),
    path('api/user_registration_patientprofile/<int:pk>/', PatientProfileRetrieveUpdateDestroyView.as_view(),
         name='patientprofile-retrieve-update-destroy'),
    path('api/user_registration_employeeprofile/', EmployeeProfileListCreateView.as_view(), name='employeeprofile-list-create'),
    path('api/user_registration_employeeprofile/<int:pk>/', EmployeeProfileRetrieveUpdateDestroyView.as_view(),
         name='employeeprofile-retrieve-update-destroy'),
    path('patient_registration_view/', patient_registration_view, name='patient_registration'),
    path('patient_login/', patient_login, name='patient_login'),
    path('patient_landing/', patient_landing, name='patient_landing'),
    path('patient_update_profile/<int:pk>/', patient_update_profile, name='patient_update_profile'),
    path('employee_registration_view/', employee_registration_view, name='employee_registration'),
    path('employee_login/', employee_login, name='employee_login'),
    path('employee_landing/', employee_landing, name='employee_landing'),
    path('employee_update_profile/<int:pk>/', employee_update_profile, name='employee_update_profile'),
    path('employee_profile/<int:pk>/', employee_profile, name='employee_profile'),
    path('patient_profile/<int:pk>/', patient_profile, name='patient_profile'),
    path('send_billing_reminders/', send_billing_reminders, name='billing_reminders'),
    path('create_billing_reminder/', create_billing_reminder, name='create_billing_reminder'),
    path('send_appointment_reminders/', send_appointment_reminders, name='appointment_reminders'),
    path('create_appointment_reminder/', create_appointment_reminder, name='create_appointment_reminder'),
    path('appointments/', appointment_list, name='appointment_list'),
    path('appointments/<int:appointment_id>/confirm/', confirm_appointment, name='confirm_appointment'),
]
