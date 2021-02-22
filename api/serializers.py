from .models import Good, PhysicalPerson, LegalPerson
from rest_framework import serializers


class PhysicalPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalPerson
        fields = ['id', 'cpf', 'name', 'zipcode', 'email', 'phone_number']


class LegalPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalPerson
        fields = [
            'id',
            'cnpj',
            'social_reason',
            'fantasy_name',
            'state_registration',
            'owner',
            'zipcode',
            'email',
            'phone_number',
        ]


class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = ['id', 'good_type', 'description', 'owner']
