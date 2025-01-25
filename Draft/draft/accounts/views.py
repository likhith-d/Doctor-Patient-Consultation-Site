from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import DoctorRegisterForm, LoginForm, PatientRegisterForm
from .models import Doctor, Patient
# views.py
from django.shortcuts import render, redirect
from .models import PatientRequest, Doctor
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import PatientRequest

@login_required
def doctor_landing(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    doctor = Doctor.objects.get(user=request.user)
    spe = doctor.Specialisation

    return render(request, 'doctor_landing.html',{
        'first_name': first_name,
        'last_name': last_name,
        'spe': spe,
    })

@login_required
def patient_landing(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    patient = Patient.objects.get(user=request.user)

    return render(request, 'patient_landing.html',{
        'first_name': first_name,
        'last_name': last_name,
    })

def show_specializations(request):
    form = DoctorRegisterForm()
    specializations = dict(form.fields['Specialisation'].choices)  # Get specializations from the form
    return render(request, 'specializations.html', {'specializations': specializations})

def show_doctors(request, specialization):
    doctors = Doctor.objects.filter(Specialisation=specialization)  # Get doctors by specialization
    return render(request, 'doctors.html', {'doctors': doctors, 'specialization': specialization})

# views.py
from django.shortcuts import render, redirect
from .models import PatientRequest, Doctor

def patient_request_view(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)

    if request.method == 'POST':
        symptoms = request.POST.get('symptoms')
        patient_name = request.user.first_name + ' ' + request.user.last_name  # Assuming the patient is logged in

        # Create a new patient request
        patient_request = PatientRequest.objects.create(
            doctor=doctor,
            patient_name=patient_name,
            symptoms=symptoms
        )

        return redirect('success_page')  # Redirect to the success page after submission

    return render(request, 'patient_request.html', {'doctor': doctor})

def success_page(request):
    return render(request, 'success_page.html')

def DoctorRegister(request):
    if request.method == 'POST':
        form = DoctorRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            Specialisation = form.cleaned_data.get('Specialisation')
            Doctor.objects.create(user=user, Specialisation=Specialisation)
            auth_login(request, user)  # Automatically log in the user after registration
            return redirect('doctor_landing')  # Redirect to doctor landing page after registration
    else:
        form = DoctorRegisterForm()
    return render(request, 'register.html', {'form': form})

def PatientRegister(request):
    if request.method == 'POST':
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save the User object without committing
            user.save()  # Save the User object to the database
            # Create a Patient linked to this User
            Patient.objects.create(user=user)
            auth_login(request, user)  # Automatically log in the user after registration
            return redirect('patient_landing')  # Redirect to patient landing page after registration
    else:
        form = PatientRegisterForm()
    return render(request, 'patient_register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Log in the user

            # Check if the user is a Doctor
            if Doctor.objects.filter(user=user).exists():
                return redirect('doctor_landing')

            # Check if the user is a Patient
            elif Patient.objects.filter(user=user).exists():
                return redirect('patient_landing')

            # Default redirection if neither doctor nor patient
            return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def doctor_requests_view(request):
    doctor = Doctor.objects.get(user=request.user)
    patient_requests = PatientRequest.objects.filter(doctor=doctor)
    return render(request, 'doctor_requests.html', {'patient_requests': patient_requests})

def home(request):
    return render(request, 'home.html')
def delete_patient_request(request, request_id):
    # Fetch the patient request by ID
    patient_request = get_object_or_404(PatientRequest, id=request_id)

    # Check if the logged-in user is the assigned doctor for this request
    if patient_request.doctor.user != request.user:
        # Optionally, you could return an error page or redirect to the home page
        return redirect('home')

    # Delete the request
    patient_request.delete()

    # Redirect back to the doctor requests page after deletion
    return redirect('doctor_requests')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# A simple view to respond to user input
@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '').lower()
        # Simple rule-based logic for responses
        if 'hello' in user_message.lower():
            bot_reply = "Hi! How can I assist you today?"
        elif 'how are you' in user_message.lower():
            bot_reply = "I'm good, thank you! How can I help you?"
        elif 'help' in user_message.lower():
            bot_reply = "Sure! What do you need help with?"
        elif 'pain' in user_message.lower():
            bot_reply = "You Need To Consult A Doctor."
        else:
            bot_reply = "I'm sorry, I didn't understand that."

        return JsonResponse({'message': bot_reply})

    return JsonResponse({'message': 'Invalid request'}, status=400)

