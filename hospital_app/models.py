from django.db import models


    #patient
'''
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
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    #doctor model

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100,null=True,blank=True)
    experience = models.IntegerField()  # Years of experience
    contact = models.CharField(max_length=20)
    room_number = models.CharField(max_length=10, blank=True, null=True)
    patients = models.ManyToManyField('Patient', blank=True)

    def __str__(self):
        return self.name
'''


# In Doctor model:
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, default="General")
    experience = models.IntegerField(default=0)
    contact = models.CharField(max_length=15, default="Not Provided")
    room_number = models.CharField(max_length=10, default="Not Assigned")

    def __str__(self):
        return self.name


#  Patient model:
class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=15)  # Ensure this field exists
    address = models.TextField()
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)  # Make sure this field exists
    medical_history = models.TextField()  # Ensure this field exists

    def __str__(self):
        return self.name



    #appointment

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    problem = models.TextField() 
    fee = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=50, choices=[("Pending", "Pending"), ("Completed", "Completed")])

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} - {self.date}"
