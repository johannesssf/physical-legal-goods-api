import json

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

CPF_REGEX = RegexValidator(r'^\d{11}$', 'Invalid CPF format.')
CNPJ_REGEX = RegexValidator(r'^\d{14}$', 'Invalid CNPJ format.')
STATE_REG_REGEX = RegexValidator(r'^\d{9}$', 'Invalid State Reg. format.')
ZIPCODE_REGEX = RegexValidator(r'^\d{8}$', 'Invalid zipcode format.')
PHONE_NUMBER_REGEX = RegexValidator(r'^\d{10,12}$', 'Invalid phone number.')
OWNER_REGEX = RegexValidator(
    r'^\d{11,14}$',
    'Invalid owner, must be a cpf or cnpj.',
)


class PhysicalPerson(models.Model):
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[CPF_REGEX],
    )
    name = models.CharField(max_length=200)
    zipcode = models.CharField(
        max_length=8,
        validators=[ZIPCODE_REGEX],
    )
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=12,
        validators=[PHONE_NUMBER_REGEX],
    )


class LegalPerson(models.Model):
    cnpj = models.CharField(
        max_length=14,
        unique=True,
        validators=[CNPJ_REGEX],
    )
    social_reason = models.CharField(max_length=200)
    fantasy_name = models.CharField(max_length=200)
    state_registration = models.CharField(
        max_length=9,
        validators=[STATE_REG_REGEX],
    )
    zipcode = models.CharField(
        max_length=8,
        validators=[ZIPCODE_REGEX],
    )
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=12,
        validators=[PHONE_NUMBER_REGEX],
    )
    owner = models.CharField(max_length=14, validators=[OWNER_REGEX])


class Good(models.Model):
    GOODS_TYPE = [
        ('imovel', 'imovel'),
        ('automovel', 'automovel'),
        ('empresa', 'empresa')
    ]
    good_type = models.CharField(max_length=9, choices=GOODS_TYPE)
    description = models.TextField()
    owner = models.CharField(max_length=14, validators=[OWNER_REGEX])
