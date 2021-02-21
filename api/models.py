from django.db import models


class PhysicalPerson(models.Model):
    cpf = models.CharField(max_length=11, unique=True)
    name = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=8)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)


class LegalPerson(models.Model):
    cnpj = models.CharField(max_length=14, unique=True)
    social_reason = models.CharField(max_length=200)
    fantasy_name = models.CharField(max_length=200)
    state_registration = models.CharField(max_length=12)
    zipcode = models.CharField(max_length=8)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)
    # See the best way to assure this value
    owner = models.CharField(max_length=14)


class Good(models.Model):
    GOODS_TYPE = [
        ('imovel', 'imovel'),
        ('automovel', 'automovel'),
        ('empresa', 'empresa')
    ]
    good_type = models.CharField(max_length=9, choices=GOODS_TYPE)
    description = models.TextField()
    # See the best way to assure this value
    owner = models.CharField(max_length=14)
