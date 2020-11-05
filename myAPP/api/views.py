import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import PatientInfo, Profile, MedicalFile, GrossDiagnosisModel
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
    用户列表
    """
    queryset = Profile.objects.all()
    serializer_class = UserProfileListSerializer


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
    用户信息详情、修改
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
    病人列表
    """
    queryset = PatientInfo.objects.all()
    serializer_class = PatientListSerializer


class PatientRUView(generics.RetrieveUpdateAPIView):
    """
    病人信息详情、修改
    每个用户（医生）都能看到所有的病人，需要传入id
    """
    queryset = PatientInfo.objects.all()
    serializer_class = PatientDetailSerializer


class GrossDiagnosisModelCreatView(generics.CreateAPIView):
    """
    创建模版
    """
    serializer_class = GrossDiagnosisModelSerializer


class GrossDiagnosisModelListView(generics.ListAPIView):
    """
    模版列表
    """
    queryset = GrossDiagnosisModel.objects.all()
    serializer_class = GrossDiagnosisModelListSerializer


class GrossDiagnosisModelRUView(generics.RetrieveUpdateAPIView):
    """
    模版详情  get
    修改  post
    """
    queryset = GrossDiagnosisModel.objects.all()
    serializer_class = GrossDiagnosisModelSerializer


class MedicalFileLCView(generics.ListCreateAPIView):
    """
    创建 post
    列表 get
    将列表和创建放在一起，因为本表的字段较少，列表中不需要省略
    且不需要修改、详情
    """
    queryset = MedicalFile.objects.all()
    serializer_class = MedicalFileSerializer

    def perform_create(self, serializer):
        # 传入参数中有一个patient即可，内容为id
        patient = serializer.validated_data.get('patient')
        serializer.save(patient=patient)


class GrossReportCreatView(generics.CreateAPIView):
    """
    创建大体报告
    """
    serializer_class = GrossReportSerializer

    def perform_create(self, serializer):
        doctor = self.request.user
        medical_file = serializer.validated_data.get('medicalFile')
        serializer.save(doctor=doctor, medicalFile=medical_file, )


class MaterialsCreatView(generics.CreateAPIView):
    """
    创建取材信息
    """
    serializer_class = MaterialsSerializer

    def perform_create(self, serializer):
        operator = self.request.user
        gross_report = serializer.validated_data.get('grossReport')
        serializer.save(operator=operator, grossReport=gross_report, )


class BiopsyCreatView(generics.CreateAPIView):
    """
    创建切片信息
    """
    serializer_class = BiopsySerializer

    def perform_create(self, serializer):
        operator = self.request.user
        materials = serializer.validated_data.get('materials')
        serializer.save(operator=operator, grossReport=materials, )


class DiagnosisReportCreatView(generics.CreateAPIView):
    """
    创建诊断报告
    """
    serializer_class = DiagnosisReportSerializer

    def perform_create(self, serializer):
        doctor = self.request.user
        medical_file = serializer.validated_data.get('medicalFile')
        serializer.save(doctor=doctor, medicalFile=medical_file, )


'''
以上应该没问题了
'''
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
