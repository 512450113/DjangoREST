import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import PatientInfo, Profile, MedicalFile, GrossDiagnosisModel, GrossReport, Materials, Biopsy, \
    DiagnosisReport
from api.serializers import PatientListSerializer, UserProfileListSerializer, UserProfileDetailSerializer, \
    UserSerializer, PatientDetailSerializer, GrossDiagnosisModelSerializer, GrossDiagnosisModelListSerializer, \
    MedicalFileSerializer, GrossReportSerializer, MaterialsSerializer, BiopsySerializer, DiagnosisReportSerializer, \
    ChangePasswordSerializer


class UserCreatView(generics.CreateAPIView):
    """
    创建用户
    """
    serializer_class = UserSerializer


class UserListView(generics.ListAPIView):
    """
    用户List
    """
    queryset = Profile.objects.all()
    serializer_class = UserProfileListSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('name', 'sex', 'created', 'updated', 'title', 'office',)
    search_fields = ('name',)
    ordering = ('id',)


class ChangePasswordView(generics.UpdateAPIView):
    """
    修改密码
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoRUView(generics.RetrieveUpdateAPIView):
    """
    用户信息RU
    """
    serializer_class = UserProfileDetailSerializer

    def get_object(self):
        # 需要登录，自己只能查看、修改自己的
        user = self.request.user
        obj = Profile.objects.get(user=user)
        return obj


class PatientCreateView(generics.CreateAPIView):
    """
    病人信息创建
    """
    serializer_class = PatientDetailSerializer


class PatientListView(generics.ListAPIView):
    """
    病人List
    """
    queryset = PatientInfo.objects.all()
    serializer_class = PatientListSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('name', 'sex', 'created', 'updated', )
    search_fields = ('name', 'address',)
    ordering = ('id',)


class PatientRUView(generics.RetrieveUpdateAPIView):
    """
    病人信息RU
    每个用户（医生）都能看到所有的病人，需要传入id
    """
    queryset = PatientInfo.objects.all()
    serializer_class = PatientDetailSerializer


class GrossDiagnosisModelCreatView(generics.CreateAPIView):
    """
    创建模版
    """
    serializer_class = GrossDiagnosisModelSerializer

    def perform_create(self, serializer):
        doctor = self.request.user
        serializer.save(doctor=doctor)


class GrossDiagnosisModelListView(generics.ListAPIView):
    """
    模版List
    """
    serializer_class = GrossDiagnosisModelListSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('doctor', 'name', 'category', 'created', 'updated', )
    search_fields = ('name', 'doctor_name', )
    ordering = ('id',)

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = GrossDiagnosisModel.objects.filter(category=category)
        else:
            queryset = GrossDiagnosisModel.objects.all()
        return queryset


class GrossDiagnosisModelRUView(generics.RetrieveUpdateAPIView):
    """
    模版RU
    """
    queryset = GrossDiagnosisModel.objects.all()
    serializer_class = GrossDiagnosisModelSerializer


class MedicalFileLCView(generics.ListCreateAPIView):
    """
    病理档案LC
    创建 post
    列表 get
    """
    queryset = MedicalFile.objects.all()
    serializer_class = MedicalFileSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('patient_name', 'created', 'updated', )
    search_fields = ('patient_name',)
    ordering = ('id',)

    def perform_create(self, serializer):
        # 传入参数中有一个patient即可，内容为id
        patient = serializer.validated_data.get('patient')
        serializer.save(patient=patient)


class GrossReportLCView(generics.ListCreateAPIView):
    """
    大体报告
    创建 POST
    列表 GET
    """
    queryset = GrossReport.objects.all()
    serializer_class = GrossReportSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('doctor_name', 'created',)
    search_fields = ('doctor_name', )
    ordering = ('id',)

    def perform_create(self, serializer):
        doctor = self.request.user
        medical_file = serializer.validated_data.get('medicalFile')
        serializer.save(doctor=doctor, medicalFile=medical_file, )


class MaterialsLCView(generics.ListCreateAPIView):
    """
    取材信息
    创建 POST
    列表 GET
    """
    queryset = Materials.objects.all()
    serializer_class = MaterialsSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('operator_name', 'created',)
    search_fields = ('operator_name', 'area')
    ordering = ('id',)

    def perform_create(self, serializer):
        operator = self.request.user
        gross_report = serializer.validated_data.get('grossReport')
        serializer.save(operator=operator, grossReport=gross_report, )


class BiopsyLCView(generics.ListCreateAPIView):
    """
    切片信息
    创建 POST
    列表 GET
    """
    queryset = Biopsy.objects.all()
    serializer_class = BiopsySerializer
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('operator_name', 'created',)
    search_fields = ('operator_name', 'area')
    ordering = ('id',)

    def perform_create(self, serializer):
        operator = self.request.user
        materials = serializer.validated_data.get('materials')
        serializer.save(operator=operator, materials=materials, )


class DiagnosisReportLCView(generics.ListCreateAPIView):
    """
    诊断报告
    创建 POST
    列表 GET
    """
    queryset = DiagnosisReport.objects.all()
    serializer_class = DiagnosisReportSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('doctor_name', 'created', 'category',)
    search_fields = ('operator_name',)
    ordering = ('id',)

    def perform_create(self, serializer):
        doctor = self.request.user
        medical_file = serializer.validated_data.get('medicalFile')
        serializer.save(doctor=doctor, medicalFile=medical_file, )


'''
以上应该没问题了
'''


class GrossReportRetrieveView(generics.RetrieveAPIView):
    """
    大体报告详情
    """
    queryset = GrossReport.objects.all()
    serializer_class = GrossReportSerializer


class MaterialsRetrieveView(generics.RetrieveAPIView):
    """
    创建取材信息详情
    """
    queryset = Materials.objects.all()
    serializer_class = MaterialsSerializer


class BiopsyRetrieveView(generics.RetrieveAPIView):
    """
    切片信息详情
    """
    queryset = Biopsy.objects.all()
    serializer_class = BiopsySerializer


class DiagnosisReportRetrieveView(generics.RetrieveAPIView):
    """
    诊断报告详情
    """
    queryset = DiagnosisReport.objects.all()
    serializer_class = DiagnosisReportSerializer


# class UserInfoView(APIView):
#     """
#     用户基本信息，仅本人可查看
#     """
#     # permission_classes = permissions.IsAuthenticated
#
#     def get(self, request):
#         user = self.request.user
#         profile = Profile.objects.get(user=user)
#         serializer = UserProfileDetailSerializer(profile)
#         # serializer = UserInfoSerializer(user)
#         # 这里的Response引用对不对？
#         return Response(serializer.data)
