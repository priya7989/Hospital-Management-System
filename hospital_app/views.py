from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Doctor, Appointment
from .forms import PatientForm, DoctorForm, AppointmentForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

# No need for a custom view if you're using Django's built-in LoginView

def home(request):
    return render(request, 'hospital_app/home.html')

# login
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

# index
def index_view(request):
    return render(request, 'hospital_app/index.html')

# Patient CRUD

# View to display the list of patients
def patients_list(request):
    patients = Patient.objects.all()
    return render(request, 'hospital_app/patients.html', {'patients': patients})

# View to handle adding a new patient
def add_patient(request):
    if request.method == 'POST':
        # Get the doctor ID from the form
        doctor_id = request.POST.get('doctor')

        # Handle case where 'Not Assigned' is selected (empty string)
        doctor = None
        if doctor_id:
            doctor = Doctor.objects.get(id=doctor_id)

        # Now create the patient object
        patient = Patient(
            name=request.POST['name'],
            age=request.POST['age'],
            gender=request.POST['gender'],
            contact=request.POST['contact'],
            address=request.POST['address'],
            medical_history=request.POST['medical_history'],
            doctor=doctor,  # This can be None if no doctor is assigned
        )
        patient.save()

        return redirect('patients_list')  # Redirect to the patient list page
    else:
        doctors = Doctor.objects.all()  # Get all doctors to display in the dropdown
        return render(request, 'hospital_app/add_patient.html', {'doctors': doctors})

# View to handle editing a patient
def edit_patient(request, id):
    # Get the patient object with the given ID
    patient = get_object_or_404(Patient, id=id)
    
    if request.method == 'POST':
        # Update the patient information if the form is submitted
        patient.name = request.POST.get('name')
        patient.age = request.POST.get('age')
        patient.gender = request.POST.get('gender')
        patient.contact = request.POST.get('contact')
        patient.medical_history = request.POST.get('medical_history')
        doctor_id = request.POST.get('doctor')
        
        # Check if doctor is assigned or 'not assigned'
        if doctor_id == 'not_assigned':
            patient.doctor = None
        else:
            patient.doctor = Doctor.objects.get(id=doctor_id)
        
        patient.save()  # Save the updated patient details

        return redirect('patients_list')  # Redirect to the patient list page

    # Render the edit patient page with existing patient details
    return render(request, 'hospital_app/edit_patient.html', {'patient': patient})

# View to handle deleting a patient
def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        patient.delete()
        return redirect('patients_list')  # Redirect to patients list after deleting

    return render(request, 'hospital_app/delete_patient.html', {'patient': patient})

# View to display detailed patient info
def patient_info(request, patient_id):
    
    patient = get_object_or_404(Patient, id=patient_id)
    
    return render(request, 'hospital_app/patient_info.html', {'patient': patient})

#select patient

def select_patient(request, patient_id):
    # Store patient ID in session
    request.session['patient_id'] = patient_id
    return redirect('patient_info')


# Doctor CRUD

# List all doctors
def doctor_list(request):
    doctors = Doctor.objects.all()  # Retrieve all doctors
    return render(request, 'hospital_app/doctor_list.html', {'doctors': doctors})

# Add a new doctor
def add_doctor(request):
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'hospital_app/add_doctor.html', {'form': form})

# Appointment CRUD

# List all appointments
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'hospital_app/appointment_list.html', {'appointments': appointments})

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

