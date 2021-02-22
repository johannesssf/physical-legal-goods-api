from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models import Good, LegalPerson, PhysicalPerson
from .serializers import (
    GoodSerializer,
    LegalPersonSerializer,
    PhysicalPersonSerializer
)


@csrf_exempt
def physical_people_list(request):
    """
    List all physical people, or create a new record.
    """
    if request.method == 'GET':
        records = PhysicalPerson.objects.all()
        serializer = PhysicalPersonSerializer(records, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PhysicalPersonSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def physical_people_detail(request, id):
    """
    Retrieve, update or delete a physical person.
    """
    try:
        physical_person = PhysicalPerson.objects.get(pk=id)
    except PhysicalPerson.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PhysicalPersonSerializer(physical_person)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PhysicalPersonSerializer(physical_person, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        physical_person.delete()
        return HttpResponse(status=200)


@csrf_exempt
def legal_people_list(request):
    """
    List all legal people, or create a new record.
    """
    if request.method == 'GET':
        records = LegalPerson.objects.all()
        serializer = LegalPersonSerializer(records, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LegalPersonSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def legal_people_detail(request, id):
    """
    Retrieve, update or delete a legal person.
    """
    try:
        legal_person = LegalPerson.objects.get(pk=id)
    except LegalPerson.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = LegalPersonSerializer(legal_person)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LegalPersonSerializer(legal_person, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        legal_person.delete()
        return HttpResponse(status=200)


@csrf_exempt
def goods_list(request):
    """
    List all goods, or create a new record.
    """
    if request.method == 'GET':
        records = Good.objects.all()
        serializer = GoodSerializer(records, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = GoodSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def goods_detail(request, id):
    """
    Retrieve, update or delete a good.
    """
    try:
        good = Good.objects.get(pk=id)
    except Good.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = GoodSerializer(good)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = GoodSerializer(good, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        good.delete()
        return HttpResponse(status=200)
