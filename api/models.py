from django.db import models

class PhysicalPerson(models.Model):
    cpf = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=8)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)
