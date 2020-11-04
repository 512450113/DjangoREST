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


class UserProfileListSerializer(serializers.ModelSerializer):
    """
    Profile序列器
    概括，用于列表展示
    医生的个人信息表
    """
    class Meta:
        model = Profile
        fields = ('id', 'name', 'sex', 'user')
        read_only_fields = ('created', 'updated',)


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
    列表，粗略
    """

    class Meta:
        model = GrossDiagnosisModel
        fields = ('id', 'doctor', 'category', 'name', 'created', 'updated',)
        read_only_fields = ('created', 'updated',)


class GrossDiagnosisModelSerializer(serializers.ModelSerializer):
    """
    GrossDiagnosisModel序列器
    诊断/大体模板表
    """

    class Meta:
        model = GrossDiagnosisModel
        fields = ('id', 'doctor', 'category', 'name', 'detail', 'created', 'updated',)
        read_only_fields = ('created', 'updated',)


class MedicalFileSerializer(serializers.ModelSerializer):
    """
    MedicalFile序列器
    病理档案表
    """

    class Meta:
        model = MedicalFile
        fields = ('id', 'patient', 'created', 'updated',)
        read_only_fields = ('created', 'updated',)


class GrossReportSerializer(serializers.ModelSerializer):
    """
    GrossReport序列器
    大体报告表
    """

    class Meta:
        model = GrossReport
        fields = ('id', 'doctor', 'detail', 'medicalFile',)
        read_only_fields = ('doctor', 'created',)


class MaterialsSerializer(serializers.ModelSerializer):
    """
    Materials序列器
    取材信息表
    """

    class Meta:
        model = Materials
        fields = ('id', 'operator', 'area', 'request', 'detail',)
        read_only_fields = ('operator', 'created',)


class BiopsySerializer(serializers.ModelSerializer):
    """
    Biopsy序列器
    切片信息表
    """

    class Meta:
        model = Biopsy
        fields = ('id', 'operator', 'area', 'dyeingMethod', 'detail',)
        read_only_fields = ('operator', 'created',)


class DiagnosisReportSerializer(serializers.ModelSerializer):
    """
    DiagnosisReport序列器
    诊断报告表
    """

    class Meta:
        model = DiagnosisReport
        fields = ('id', 'doctor', 'category', 'detail',)
        read_only_fields = ('doctor', 'created',)
