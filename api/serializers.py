from .models import PhysicalPerson
from rest_framework import serializers


class PhysicalPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalPerson
        fields = ['id', 'cpf', 'name', 'zipcode', 'email', 'phone_number']
