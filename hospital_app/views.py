from django.shortcuts import render, redirect,get_object_or_404
from .models import Patient, Doctor, Appointment
from .forms import PatientForm, DoctorForm, AppointmentForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
 


# No need for a custom view if you're using Django's built-in LoginView





def home_view(request):
    return render(request, 'hospital_app/home.html')


#login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to your desired page after login
            else:
                # Invalid credentials
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    return render(request, 'hospital_app/login.html', {'form': form})

#index
def index_view(request):
    return render(request, 'hospital_app/index.html')

# Patient CRUD

def patients_list(request):
    patients = Patient.objects.all()  # Fetch all patients
    return render(request, 'hospital_app/patients.html', {'patients': patients})

def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients_list')  # Redirect after successful submission
    else:
        form = PatientForm()
    
    return render(request, 'hospital_app/add_patient.html', {'form': form})
# Doctor CRUD


def doctor_list(request):
    doctors = Doctor.objects.all()  # Fetch all doctors from DB
    return render(request, 'doctor_list.html', {'doctors': doctors})

def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'add_doctor.html', {'form': form})

# Appointment CRUD
# List all appointments
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointments.html', {'appointments': appointments})

# Add a new appointment

def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'hospital_app/add_appointment.html', {'form': form})



# Update an existing appointment
def update_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'hospital_app/update_appointment.html', {'form': form})


# Delete an appointment
def delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)  # Fetch the appointment by id
    
    if request.method == 'POST':
        appointment.delete()  # Delete the appointment
        return redirect('appointment_list')  # Redirect to the appointment list
    
    return render(request, 'hospital_app/delete_appointment.html', {'appointment': appointment})


