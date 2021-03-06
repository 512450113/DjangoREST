from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import PatientInfo, GrossDiagnosisModel, MedicalFile, GrossReport, Materials, Biopsy, \
    DiagnosisReport, Profile

'''
备忘：创建的序列器是User，列表和修改是Profile
'''


class UserSerializer(serializers.ModelSerializer):
    """
    创建用户，自定义create，要求同时创建医生的个人信息表
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        profile = Profile(user=user)
        profile.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """
    用于修改密码
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserProfileListSerializer(serializers.ModelSerializer):
    """
    Profile序列器
    概括，用于列表展示
    医生的个人信息表
    """
    account_number = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = ('id', 'name', 'sex', 'user', 'account_number', 'title', 'office')


class UserProfileDetailSerializer(serializers.ModelSerializer):
    """
    Profile序列器
    详细信息
    医生信息表，仅本人可查看
    """

    class Meta:
        model = Profile
        fields = ('id', 'name', 'sex', 'phoneNumber', 'title', 'office',)
        read_only_fields = ('created', 'updated',)


class PatientListSerializer(serializers.ModelSerializer):
    """
    PatientInfo序列器
    概括，用于列表展示
    患者信息表
    """

    class Meta:
        model = PatientInfo
        fields = ('id', 'name', 'sex',)
        read_only_fields = ('created', 'updated',)


class PatientDetailSerializer(serializers.ModelSerializer):
    """
    PatientInfo序列器
    详细信息
    患者信息表
    """

    class Meta:
        model = PatientInfo
        fields = ('id', 'name', 'sex', 'phoneNumber', 'address',)
        read_only_fields = ('created', 'updated',)


class GrossDiagnosisModelListSerializer(serializers.ModelSerializer):
    """
    GrossDiagnosisModel序列器
    诊断/大体模板表
    用于展示粗略列表
    """
    doctorName = serializers.CharField(source='doctor.doctor_info_of.name')

    class Meta:
        model = GrossDiagnosisModel
        fields = ('id', 'doctor', 'doctorName', 'category', 'name', 'created', 'updated',)
        read_only_fields = ('created', 'updated',)


class GrossDiagnosisModelSerializer(serializers.ModelSerializer):
    """
    GrossDiagnosisModel序列器
    诊断/大体模板表
    用于创建
    """
    doctorName = serializers.CharField(source='doctor.doctor_info_of.name', read_only=True)

    class Meta:
        model = GrossDiagnosisModel
        fields = ('id', 'doctor', 'doctorName', 'category', 'name', 'detail', 'created', 'updated',)
        read_only_fields = ('created', 'updated', 'doctor')


class MedicalFileSerializer(serializers.ModelSerializer):
    """
    MedicalFile
    病理档案表
    """
    patientName = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = MedicalFile
        fields = ('id', 'patient', 'patientName', 'created', 'updated',)
        read_only_fields = ('created', 'updated', )


class GrossReportSerializer(serializers.ModelSerializer):
    """
    GrossReport
    大体报告表
    """
    doctorName = serializers.CharField(source='doctor.doctor_info_of.name', read_only=True)
    patient = serializers.CharField(source='medicalFile.patient.name', read_only=True)

    class Meta:
        model = GrossReport
        fields = ('id', 'doctor', 'doctorName', 'patient', 'detail', 'medicalFile', 'created',)
        read_only_fields = ('doctor', 'created',)


class MaterialsSerializer(serializers.ModelSerializer):
    """
    Materials序列器
    取材信息表
    """
    operatorName = serializers.CharField(source='operator.doctor_info_of.name', read_only=True)

    class Meta:
        model = Materials
        fields = ('id', 'operator', 'operatorName',  'grossReport', 'area', 'request', 'detail', 'created',)
        read_only_fields = ('operator', 'created',)


class BiopsySerializer(serializers.ModelSerializer):
    """
    Biopsy序列器
    切片信息表
    """
    operatorName = serializers.CharField(source='operator.doctor_info_of.name', read_only=True)

    class Meta:
        model = Biopsy
        fields = ('id', 'operator', 'operatorName', 'area', 'materials', 'dyeingMethod', 'detail', 'created',)
        read_only_fields = ('operator', 'created',)


class DiagnosisReportSerializer(serializers.ModelSerializer):
    """
    DiagnosisReport序列器
    诊断报告表
    """
    doctorName = serializers.CharField(source='doctor.doctor_info_of.name', read_only=True)

    class Meta:
        model = DiagnosisReport
        fields = ('id', 'doctor', 'doctorName', 'medicalFile', 'category', 'detail', 'created',)
        read_only_fields = ('doctor', 'created',)
