from django.contrib import admin
from django.urls import path, include

from api import views

urlpatterns = [
    path('userCreate/', views.UserCreatView.as_view(), name='userCreate'),
    path('userList/', views.UserListView.as_view(), name='userList'),
    path('changePassword/', views.ChangePasswordView.as_view(), name='changePassword'),
    path('userInfoRU/<int:pk>/', views.UserInfoRUView.as_view(), name='userInfoRU'),


    path('patientCreate/', views.PatientCreateView.as_view(), name='patientCreate'),
    path('patientList/', views.PatientListView.as_view(), name='patientList'),
    path('patientRU/<int:pk>/', views.PatientRUView.as_view(), name='patientRU'),

    path('grossDiagnosisModelCreat/', views.GrossDiagnosisModelCreatView.as_view(), name='grossDiagnosisModelCreat'),
    path('grossDiagnosisModelList/', views.GrossDiagnosisModelListView.as_view(), name='grossDiagnosisModelList'),
    path('grossDiagnosisModelRU/<int:pk>/', views.GrossDiagnosisModelRUView.as_view(), name='grossDiagnosisModelRU'),

    path('medicalFileLC/', views.MedicalFileLCView.as_view(), name='medicalFileLC'),
    path('grossReportCreat/', views.GrossReportCreatView.as_view(), name='grossReportCreat'),
    path('biopsyCreat/', views.BiopsyCreatView.as_view(), name='biopsyCreat'),
    path('diagnosisReportCreat/', views.DiagnosisReportCreatView.as_view(), name='diagnosisReportCreat'),
    # path('patientList/', views.PatientListView.as_view(), name='patientList'),
    # path('patientRU/<int:pk>/', views.PatientRUView.as_view(), name='patientRU'),

    # path('userCreate/', views.UserCreatView.as_view(), name='userCreate'),
    # path('', ),
    # path('index', views.index, name='index'),
]