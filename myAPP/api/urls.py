from django.contrib import admin
from django.urls import path, include

from api import views

urlpatterns = [
    # 用户
    path('userCreate/', views.UserCreatView.as_view(), name='userCreate'),
    path('userList/', views.UserListView.as_view(), name='userList'),
    path('changePassword/', views.ChangePasswordView.as_view(), name='changePassword'),
    path('userInfoRU/', views.UserInfoRUView.as_view(), name='userInfoRU'),

    # 病人信息
    path('patientCreate/', views.PatientCreateView.as_view(), name='patientCreate'),
    path('patientList/', views.PatientListView.as_view(), name='patientList'),
    path('patientRU/<int:pk>/', views.PatientRUView.as_view(), name='patientRU'),

    # 模版
    path('grossDiagnosisModelCreat/', views.GrossDiagnosisModelCreatView.as_view(), name='grossDiagnosisModelCreat'),
    path('grossDiagnosisModelList/', views.GrossDiagnosisModelListView.as_view(), name='grossDiagnosisModelList'),
    path('grossDiagnosisModelRU/<int:pk>/', views.GrossDiagnosisModelRUView.as_view(), name='grossDiagnosisModelRU'),

    # 病理档案
    path('medicalFileLC/', views.MedicalFileLCView.as_view(), name='medicalFileLC'),

    # 大体报告
    path('grossReportLC/', views.GrossReportLCView.as_view(), name='grossReportLC'),
    path('grossReportRetrieve/<int:pk>/', views.GrossReportRetrieveView.as_view(), name='grossReportRetrieve'),

    # 取材
    path('materialsLC/', views.MaterialsLCView.as_view(), name='materialsLC'),
    path('materialsRetrieve/<int:pk>/', views.MaterialsRetrieveView.as_view(), name='materialsRetrieve'),

    # 切片
    path('biopsyLC/', views.BiopsyLCView.as_view(), name='biopsyLC'),
    path('biopsyRetrieve/<int:pk>/', views.BiopsyRetrieveView.as_view(), name='biopsyRetrieve'),

    # 诊断报告
    path('diagnosisReportLC/', views.DiagnosisReportLCView.as_view(), name='diagnosisReportLC'),
    path('diagnosisReportRetrieve/<int:pk>/', views.DiagnosisReportRetrieveView.as_view(), name='diagnosisReportRetrieve'),

    # path('patientList/', views.PatientListView.as_view(), name='patientList'),
    # path('patientRU/<int:pk>/', views.PatientRUView.as_view(), name='patientRU'),

    # path('userCreate/', views.UserCreatView.as_view(), name='userCreate'),
    # path('', ),
    # path('index', views.index, name='index'),
]