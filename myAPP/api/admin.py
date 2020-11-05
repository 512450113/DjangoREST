from django.contrib import admin

# Register your models here.
from api.models import Profile, PatientInfo, GrossDiagnosisModel, MedicalFile, GrossReport, Materials, Biopsy, \
    DiagnosisReport


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'sex', 'phoneNumber', 'title', 'office', ]


admin.site.register(Profile, UserProfileAdmin)


class PatientInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'sex', 'phoneNumber', 'address', ]


admin.site.register(PatientInfo, PatientInfoAdmin)


class GrossDiagnosisModelAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'category', 'name', 'detail', ]


admin.site.register(GrossDiagnosisModel, GrossDiagnosisModelAdmin)


class MedicalFileAdmin(admin.ModelAdmin):
    list_display = ['patient', ]


admin.site.register(MedicalFile, MedicalFileAdmin)


class GrossReportAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'medicalFile', 'detail', ]


admin.site.register(GrossReport, GrossReportAdmin)


class MaterialsAdmin(admin.ModelAdmin):
    list_display = ['operator', 'area', 'request', 'grossReport', 'detail', ]


admin.site.register(Materials, MaterialsAdmin)


class BiopsyAdmin(admin.ModelAdmin):
    list_display = ['operator', 'area', 'dyeingMethod', 'materials', 'detail', ]


admin.site.register(Biopsy, BiopsyAdmin)


class DiagnosisReportAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'category', 'medicalFile', 'detail', ]


admin.site.register(DiagnosisReport, DiagnosisReportAdmin)
