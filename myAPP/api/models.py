from django.db import models

# Create your models here.
# from django_mysql.models import JSONField

def my_default():
    return {'foo': 'bar'}

class MyTest(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=80, blank=True, null=True)
    patient = models.CharField(max_length=80, blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    detail = models.JSONField() # default=my_default
    #dev上更新的一点东西