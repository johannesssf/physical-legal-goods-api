import json

from django.test import TestCase
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from .models import PhysicalPerson, LegalPerson, Good
from .serializers import LegalPersonSerializer, PhysicalPersonSerializer


class PhysicalPersonModelTest(TestCase):
    def test_physical_person_creation(self):
        physical_person = PhysicalPerson.objects.create(
            cpf="25845675391",
            name="Fulando Mais Sobrenome",
            zipcode="12345678",
            email="fulano@email.com",
            phone_number="11234567890"
        )
        self.assertIsNotNone(physical_person)


class LegalPersonModelTest(TestCase):
    def test_legal_person_creation(self):
        legal_person = LegalPerson.objects.create(
            cnpj="12345678900013",
            social_reason="Minha Super Empresa",
            fantasy_name="Nome Fantasia",
            state_registration="123456789012",
            zipcode="12345678",
            email="fulano@email.com",
            phone_number="11234567890",
            owner="25845675391"
        )
        self.assertIsNotNone(legal_person)


class GoodModelTest(TestCase):
    def test_good_creation(self):
        good = Good.objects.create(
            good_type="imovel",
            description="Apartamento localizado na rua X número Y.",
            owner="12345678900018"
        )
        self.assertIsNotNone(good)


class PhysicalPeopleAPITest(TestCase):
    RECORDS_NUM = 4

    def setUp(self):
        self.client = APIClient()

        for _ in range(self.RECORDS_NUM):
            physical_person = baker.make(PhysicalPerson)
            physical_person.save()

    def test_physical_people_get_list(self):
        records = PhysicalPerson.objects.all()
        request = self.client.get('/v1/physical-people/')

        self.assertEquals(request.status_code, status.HTTP_200_OK)
        self.assertEquals(len(json.loads(request.content)), len(records))

    def test_physical_people_post(self):
        new_record = {
            'cpf': '45651237863',
            'name': 'AAAAA BBBBB CCCCC',
            'zipcode': '88456329',
            'email': 'aaabbbccc@email.com',
            'phone_number': '51999853214'
        }
        request = self.client.post(
            '/v1/physical-people/',
            json.dumps(new_record),
            content_type='application/json'
        )
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        physical_person = PhysicalPerson.objects.get(cpf=new_record['cpf'])
        self.assertEquals(physical_person.cpf, new_record['cpf'])

    def test_physical_people_post_invalid_cpf(self):
        new_record = PhysicalPersonSerializer(baker.make(PhysicalPerson)).data
        new_record['cpf'] = '321654987654321'

        request = self.client.post(
            '/v1/physical-people/',
            json.dumps(new_record),
            content_type='application/json'
        )
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_physical_people_get(self):
        record = PhysicalPerson.objects.get(pk=1)
        request = self.client.get(f'/v1/physical-people/{record.id}/')
        data = json.loads(request.content)

        self.assertEquals(request.status_code, status.HTTP_200_OK)
        self.assertEquals(record.id, data['id'])
        self.assertEquals(record.cpf, data['cpf'])
        self.assertEquals(record.name, data['name'])
        self.assertEquals(record.zipcode, data['zipcode'])
        self.assertEquals(record.email, data['email'])
        self.assertEquals(record.phone_number, data['phone_number'])

    def test_physical_people_non_existent_id(self):
        request = self.client.get(f'/v1/physical-people/{999}/')
        self.assertEquals(request.status_code, 404)

    def test_physical_people_put(self):
        record = PhysicalPerson.objects.get(pk=1)
        data = PhysicalPersonSerializer(record).data
        data['zipcode'] = '11222333'
        request = self.client.put(
            f'/v1/physical-people/{data["id"]}/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        record = PhysicalPerson.objects.get(pk=1)
        self.assertEquals(record.zipcode, data['zipcode'])

    def test_physical_people_put_invalid_cpf(self):
        record = PhysicalPerson.objects.get(pk=1)
        data = PhysicalPersonSerializer(record).data
        data['cpf'] = '111222333444555'
        request = self.client.put(
            f'/v1/physical-people/{data["id"]}/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_physical_people_delete(self):
        record = PhysicalPerson.objects.get(pk=1)
        request = self.client.delete(f'/v1/physical-people/{record.id}/')

        self.assertEquals(request.status_code, status.HTTP_200_OK)
        records = PhysicalPerson.objects.filter(pk=1)
        self.assertEquals(len(records), 0)


class LegalPeopleAPITest(TestCase):
    RECORDS_NUM = 4

    def setUp(self):
        self.client = APIClient()

        for _ in range(self.RECORDS_NUM):
            physical_person = baker.make(LegalPerson)
            physical_person.save()

    def test_legal_people_get_list(self):
        records = LegalPerson.objects.all()
        request = self.client.get('/v1/legal-people/')

        self.assertEquals(request.status_code, status.HTTP_200_OK)
        self.assertEquals(len(json.loads(request.content)), len(records))

    def test_legal_people_post(self):
        new_record = {
            'cnpj': '00012345600019',
            'social_reason': 'Some New Company',
            'fantasy_name': 'Company Fantasy Name',
            'state_registration': '0123456789',
            'owner': '25845675391',
            'zipcode': '88456329',
            'email': 'newcompany@email.com',
            'phone_number': '51988853214'
        }
        request = self.client.post(
            '/v1/legal-people/',
            json.dumps(new_record),
            content_type='application/json'
        )
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        legal_person = LegalPerson.objects.get(cnpj=new_record['cnpj'])
        self.assertEquals(legal_person.cnpj, new_record['cnpj'])

    def test_legal_people_post_invalid_cnpj(self):
        new_record = LegalPersonSerializer(baker.make(LegalPerson)).data
        new_record['cnpj'] = '321654987654321111'

        request = self.client.post(
            '/v1/legal-people/',
            json.dumps(new_record),
            content_type='application/json'
        )
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_legal_people_get(self):
        record = LegalPerson.objects.get(pk=1)
        request = self.client.get(f'/v1/legal-people/{record.id}/')
        data = json.loads(request.content)

        self.assertEquals(request.status_code, status.HTTP_200_OK)
        self.assertEquals(record.id, data['id'])
        self.assertEquals(record.cnpj, data['cnpj'])
        self.assertEquals(record.social_reason, data['social_reason'])
        self.assertEquals(record.fantasy_name, data['fantasy_name'])
        self.assertEquals(record.state_registration, data['state_registration'])
        self.assertEquals(record.owner, data['owner'])
        self.assertEquals(record.zipcode, data['zipcode'])
        self.assertEquals(record.email, data['email'])
        self.assertEquals(record.phone_number, data['phone_number'])

    def test_legal_people_non_existent_id(self):
        request = self.client.get(f'/v1/legal-people/{999}/')
        self.assertEquals(request.status_code, 404)

    def test_physical_people_put(self):
        record = LegalPerson.objects.get(pk=1)
        data = LegalPersonSerializer(record).data
        data['zipcode'] = '11222333'
        request = self.client.put(
            f'/v1/legal-people/{data["id"]}/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        record = LegalPerson.objects.get(pk=1)
        self.assertEquals(record.zipcode, data['zipcode'])

    def test_legal_people_put_invalid_cpf(self):
        record = LegalPerson.objects.get(pk=1)
        data = LegalPersonSerializer(record).data
        data['cnpj'] = '111222333444555666777'
        request = self.client.put(
            f'/v1/legal-people/{data["id"]}/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_legal_people_delete(self):
        record = LegalPerson.objects.get(pk=1)
        request = self.client.delete(f'/v1/legal-people/{record.id}/')

        self.assertEquals(request.status_code, status.HTTP_200_OK)
        records = LegalPerson.objects.filter(pk=1)
        self.assertEquals(len(records), 0)
