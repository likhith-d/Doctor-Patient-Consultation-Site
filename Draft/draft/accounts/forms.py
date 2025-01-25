from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

SPEC = [
    ('cardiology', 'CARDIOLOGY'),
    ('oncology', 'ONCOLOGY'),
    ('general physician', 'GENERAL PHYSICIAN'),
    ('pediatrician', 'PEDIATRICIAN'),
]
class DoctorRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length = 50)
    last_name = forms.CharField(max_length=50)
    Specialisation = forms.ChoiceField(choices = SPEC)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'Specialisation', 'password1', 'password2']

class PatientRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length = 50)
    last_name = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']