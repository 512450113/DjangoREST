import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from api.models import MyTest


def index(request):
    username = request.GET['username']
    patient = request.GET['patient']
    typeA = request.GET['type']
    detail = request.GET['detail']
    # print(type(detail))
    # print(detail)
    # print('开始转换')
    detail = json.loads(detail)
    # print(type(detail))
    # print(detail['name'])
    result = MyTest.objects.create(
        username=username,
        patient=patient,
        type=type,
        detail=detail)

    # result = MyTest.objects.create(
    #     username='Alex',
    #     patient='Bob',
    #     type='a piece of cake',
    #     detail="""{
    #     "A": "aaa",
    #     "B": "bbb",
    #     "C": "ccc",
    #     "D": "ddd",
    #     }""")
    return HttpResponse(detail['name'])

def search(request):
    # result = MyTest.objects.filter(detail__contains={'name': 'Google'}).first()
    result = MyTest.objects.filter(detail__name='Google').first()
    # print(type(result.detail))
    return HttpResponse(result.detail['name'])