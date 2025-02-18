from django import forms
from .models import Patient, Doctor, Appointment

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'experience', 'contact', 'room_number']


class AppointmentForm(forms.ModelForm):
    
    patient_name = forms.CharField(max_length=100, label="Patient Name")
    patient_age = forms.IntegerField(label="Age")
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label="Select Doctor")
    patient_gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], label="Gender")
    patient_phone = forms.CharField(max_length=15, label="Phone")
    patient_height = forms.FloatField(label="Height (in cm)")
    patient_weight = forms.FloatField(label="Weight (in kg)")
    patient_bp = forms.CharField(max_length=20, label="Blood Pressure")
    problem = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your problem or symptoms'}), label="Problem/Symptoms", required=True)

    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    fee = forms.DecimalField(max_digits=6, decimal_places=2)
    status = forms.CharField(max_length=50, initial="Pending")

    class Meta:
        model = Appointment
        fields = ['patient_name', 'patient_age', 'patient_gender', 'patient_phone', 'patient_height', 
                  'patient_weight', 'patient_bp', 'problem', 'doctor', 'date', 'fee', 'status']  # Added 'problem'

    def save(self, commit=True):
        # Check if the patient already exists in the system by phone or other unique field
        patient, created = Patient.objects.get_or_create(
            name=self.cleaned_data['patient_name'],
            phone=self.cleaned_data['patient_phone'],  # You can change this field to your preferred unique identifier
            defaults={
                'age': self.cleaned_data['patient_age'],
                'gender': self.cleaned_data['patient_gender'],
                'height': self.cleaned_data['patient_height'],
                'weight': self.cleaned_data['patient_weight'],
                'bp': self.cleaned_data['patient_bp'],
            }
        )

        # Now create the Appointment and link it to the patient
        appointment = super().save(commit=False)
        appointment.patient = patient  # Assign the patient (either new or existing) to the appointment
        appointment.problem = self.cleaned_data['problem']  # Save the problem/symptoms description
        appointment.doctor = self.cleaned_data['doctor'] 
        if commit:
            appointment.save()  # Commit the changes to the database
        
        appointment.doctor.patients.add(patient)
        return appointment
