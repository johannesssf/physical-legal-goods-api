from django.test import TestCase

from .models import PhysicalPerson


class PhysicalPersonModel(TestCase):
    def test_model_create(self):
        physical_person = PhysicalPerson.objects.create(
            cpf="25845675391",
            name="Fulando Mais Sobrenome",
            zipcode="12345678",
            email="fulano@email.com",
            phone_number="11234567890"
        )
        self.assertIsNotNone(physical_person)
