from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Specialisation = models.CharField(max_length=50, choices=[
        ('cardiology', 'CARDIOLOGY'),
        ('oncology', 'ONCOLOGY'),
        ('general physician', 'GENERAL PHYSICIAN'),
        ('pediatrician', 'PEDIATRICIAN'),
    ])

    def __str__(self):
        return f"{self.user.username} - {self.Specialisation}"

# models.py
# models.py
from django.db import models
from django.contrib.auth.models import User

class PatientRequest(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=255)  # Assuming this is a field for patient name
    symptoms = models.TextField()

    def __str__(self):
        return f"{self.patient_name} - {self.doctor.user.first_name} {self.doctor.user.last_name}"



class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - Patient"
