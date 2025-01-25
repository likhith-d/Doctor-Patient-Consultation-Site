from django.urls import path
from . import views
from .views import chatbot_response

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.DoctorRegister, name='register'),
    path('patientregister/', views.PatientRegister, name='patient_register'),
    path('doctorlanding/', views.doctor_landing, name='doctor_landing'),
    path('patientlanding/', views.patient_landing, name='patient_landing'),
    path('specializations/', views.show_specializations, name='show_specializations'),
    path('doctors/<str:specialization>/', views.show_doctors, name='show_doctors'),
    path('doctor/<int:doctor_id>/request/', views.patient_request_view, name='patient_request'),
    path('doctor/requests/', views.doctor_requests_view, name='doctor_requests'),
    path('success/', views.success_page, name='success_page'),
    path('doctor/requests/delete/<int:request_id>/', views.delete_patient_request, name='delete_patient_request'),
    path('chatbot-response/', chatbot_response, name='chatbot_response'),
]