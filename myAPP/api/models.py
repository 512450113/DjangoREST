from django.conf import settings
from django.db import models


# Create your models here.
def my_default():
    return {'foo': 'bar'}


class Profile(models.Model):
    """
    用户详细信息表
    """
    Sex_Choice = (
        ('male', '男'),
        ('female', '女')
    )
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_info_of')
    name = models.CharField(max_length=80, blank=True, null=True, default='未命名')
    sex = models.CharField(choices=Sex_Choice, default='male', max_length=10)
    phoneNumber = models.CharField(max_length=80, blank=True, null=True, default='000')
    title = models.CharField(max_length=80, blank=True, null=True, default='主治医师')
    office = models.CharField(max_length=80, blank=True, null=True, default='未分配')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class PatientInfo(models.Model):
    """
    患者信息表
    """
    Sex_Choice = (
        ('male', '男'),
        ('female', '女')
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, blank=False, null=False)
    sex = models.CharField(choices=Sex_Choice, default='male', max_length=10)
    phoneNumber = models.CharField(max_length=80, blank=False, null=False, default='000')
    address = models.CharField(max_length=80, blank=False, null=False, default='未填写')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class GrossDiagnosisModel(models.Model):
    """
    诊断/大体模板表
    """
    Model_Choice = (
        ('Gross', '大体模版'),
        ('Diagnosis', '诊断模版')
    )
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='models_of')
    category = models.CharField(choices=Model_Choice, default='Gross', max_length=20)
    name = models.CharField(max_length=80, blank=False, null=False)
    detail = models.JSONField(default=my_default)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class MedicalFile(models.Model):
    """
    病理档案表
    """
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE, related_name='medical_file_of')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class GrossReport(models.Model):
    """
    大体报告表
    """
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gross_report_by')
    medicalFile = models.ForeignKey(MedicalFile, on_delete=models.CASCADE, related_name='gross_report_for')
    detail = models.JSONField(default=my_default)
    created = models.DateTimeField(auto_now_add=True)


class Materials(models.Model):
    """
    取材信息表
    """
    id = models.AutoField(primary_key=True)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='materials_by')
    area = models.CharField(max_length=80, blank=False, null=False)
    request = models.CharField(max_length=80, blank=False, null=False)
    grossReport = models.ForeignKey(GrossReport, on_delete=models.CASCADE, related_name='materials_of')
    detail = models.JSONField(default=my_default)
    created = models.DateTimeField(auto_now_add=True)


class Biopsy(models.Model):
    """
    切片信息表
    """
    id = models.AutoField(primary_key=True)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='biopsy_by')
    area = models.CharField(max_length=80, blank=False, null=False)
    dyeingMethod = models.CharField(max_length=80, blank=False, null=False)
    materials = models.ForeignKey(Materials, on_delete=models.CASCADE, related_name='biopsy_of')
    detail = models.JSONField(default=my_default)
    created = models.DateTimeField(auto_now_add=True)


class DiagnosisReport(models.Model):
    """
    诊断报告表
    """
    Model_Choice = (
        ('0', '初诊报告'),
        ('1', '主诊报告'),
        ('2', '特诊报告'),
    )
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='diagnosis_report_by')
    category = models.CharField(choices=Model_Choice, default='0', max_length=20)
    medicalFile = models.ForeignKey(MedicalFile, on_delete=models.CASCADE, related_name='diagnosis_report_for')
    detail = models.JSONField(default=my_default)
    created = models.DateTimeField(auto_now_add=True)
