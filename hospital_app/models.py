from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")
    bp = models.CharField(max_length=20, help_text="Blood Pressure (e.g., 120/80)")

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.department})"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    problem = models.TextField() 
    fee = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} - {self.date}"
