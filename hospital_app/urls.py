'''from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('patients/', views.patients_list, name='patients_list'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('add-doctor/', views.add_doctor, name='add_doctor'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('add-appointment/', views.add_appointment, name='add_appointment'),
]

'''




from django.urls import path
from . import views 
from .views import appointment_list, add_appointment, update_appointment, delete_appointment,doctor_list,add_doctor


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('index/', views.index_view, name='index'),
    path('doctor/', doctor_list, name='doctor_list'),
    path('add-doctor/', add_doctor, name='add_doctor'),
    path('patients/', views.patients_list, name='patients_list'),
    
    path('add-patient/', views.add_patient, name='add_patient'),
    path('edit-patient/<int:id>/', views.edit_patient, name='edit_patient'),
    path('delete-patient/<int:id>/', views.delete_patient, name='delete_patient'),
    path('appointment/', views.appointment_list, name='appointment_list'),
    path('add/', add_appointment, name='add_appointment'),
    path('update/<int:id>/', update_appointment, name='update_appointment'),
    path('delete/<int:id>/', delete_appointment, name='delete_appointment'),
    path('patient_info/', views.patient_info, name='patient_info'),
   #path('patient_info/<int:patient_id>/', views.patient_info, name='patient_info'),
]

