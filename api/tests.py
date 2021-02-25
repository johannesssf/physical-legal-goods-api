import json

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from .models import Good, LegalPerson, PhysicalPerson
from .serializers import (
    GoodSerializer,
    LegalPersonSerializer,
    PhysicalPersonSerializer
)


PHYSICAL_PERSON_DATA = {
    "cpf": "25845675391",
    "name": "Fulano Sem Sobrenome",
    "email": "fulanosemnome@email.com",
    "zipcode": "55632578",
    "phone_number": "48666325147",
}
LEGAL_PERSON_DATA = {
    "cnpj": "12345678900033",
    "social_reason": "Super Company",
    "fantasy_name": "Some Fantasy Name",
    "state_registration": "123456789555",
    "zipcode": "12345678",
    "email": "supercompany@email.com",
    "phone_number": "11234567893",
    "owner": PHYSICAL_PERSON_DATA["cpf"]
}

GOOD_DATA = {
    "good_type": "automovel",
    "description": "Fusca 66",
    "owner": LEGAL_PERSON_DATA["cnpj"]
}


class TestAPIModels(TestCase):
    """Tests to validade the API models."""

    def test_physical_person_fields_validation(self):
        physical_person = PhysicalPerson.objects.create(
            cpf="a5845675391",
            name="Fulando Mais Sobrenome",
            zipcode="a2345678",
            email="fulano@email.com",
            phone_number="a1234567890"
        )
        with self.assertRaises(ValidationError):
            physical_person.full_clean()

    def test_legal_person_fields_validation(self):
        legal_person = LegalPerson.objects.create(
            cnpj="123456789000AA",
            social_reason="Minha Super Empresa",
            fantasy_name="Nome Fantasia",
            state_registration="123456789AAA",
            zipcode="1234567A",
            email="fulano@email.com",
            phone_number="1123456789A",
            owner="123456789",
        )
        with self.assertRaises(ValidationError):
            legal_person.full_clean()


class TestAPIAuthentication(TestCase):
    """Tests the authentication access behavior."""

    def setUp(self):
        admin = get_user_model().objects.create(username='admin')
        admin.set_password('asdf!@#$')
        admin.save()

    def test_access_without_credentials(self):
        client = APIClient()
        request = client.get('/v1/physical-people/')

        self.assertEquals(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_invalid_credentials(self):
        client = APIClient()
        self.assertFalse(client.login(username="some-user", password="123456"))

    def test_login_and_access_ok(self):
        client = APIClient()
        self.assertTrue(client.login(username="admin", password="asdf!@#$"))

        request = client.get('/v1/physical-people/')
        self.assertEquals(request.status_code, status.HTTP_200_OK)

        request = client.get('/v1/legal-people/')
        self.assertEquals(request.status_code, status.HTTP_200_OK)

        request = client.get('/v1/goods/')
        self.assertEquals(request.status_code, status.HTTP_200_OK)


class TestAPIEndpoints(TestCase):
    """Tests the API endpoints."""

    def setUp(self):
        admin = get_user_model().objects.create(username='admin')
        self.client = APIClient()
        self.client.force_authenticate(user=admin)

        # A valid physical person used in tests
        self.physical_person = PhysicalPerson.objects.create(
            **PHYSICAL_PERSON_DATA,
        )

        self.legal_person = LegalPerson.objects.create(
            **LEGAL_PERSON_DATA,
        )

        self.good = Good.objects.create(
            **GOOD_DATA,
        )

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
        data['cpf'] = '25632141235'
        data['zipcode'] = '88563214'
        data['phone_number'] = '63222125478'
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

    def test_legal_people_get_list(self):
        records = LegalPerson.objects.all()
        request = self.client.get('/v1/legal-people/')

        self.assertEquals(request.status_code, status.HTTP_200_OK)
        self.assertEquals(len(json.loads(request.content)), len(records))

    def test_legal_people_post(self):
        new_record = LegalPersonSerializer({
            'cnpj': '00012345600019',
            'social_reason': 'Some New Company',
            'fantasy_name': 'Company Fantasy Name',
            'state_registration': '256396584',
            'zipcode': '88456329',
            'email': 'newcompany@email.com',
            'phone_number': '51988853214',
            'owner': self.physical_person.cpf,
        }).data
        request = self.client.post(
            '/v1/legal-people/',
            json.dumps(new_record),
            content_type='application/json'
        )
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        legal_person = LegalPerson.objects.get(cnpj=new_record['cnpj'])
        self.assertEquals(legal_person.cnpj, new_record['cnpj'])

    def test_legal_people_post_invalid_data(self):
        new_record = LegalPersonSerializer(baker.make(LegalPerson)).data

        request = self.client.post(
            '/v1/legal-people/',
            json.dumps(new_record),
            content_type='application/json'
        )
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_legal_people_post_invalid_owner(self):
        new_record = LegalPersonSerializer({
            "cnpj": "12365447833325",
            "social_reason": "Super Company",
            "fantasy_name": "Some Fantasy Name",
            "state_registration": "125695478",
            "zipcode": "12345678",
            "email": "supercompany@email.com",
            "phone_number": "11234567893",
            "owner": "22255599977",
        }).data

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
        self.assertEquals(
            record.state_registration,
            data['state_registration'],
        )
        self.assertEquals(record.owner, data['owner'])
        self.assertEquals(record.zipcode, data['zipcode'])
        self.assertEquals(record.email, data['email'])
        self.assertEquals(record.phone_number, data['phone_number'])

    def test_legal_people_non_existent_id(self):
        request = self.client.get(f'/v1/legal-people/{999}/')
        self.assertEquals(request.status_code, 404)

    def test_legal_people_put(self):
        record = LegalPerson.objects.get(pk=1)
        data = LegalPersonSerializer(record).data
        data['cnpj'] = '32854762302108'
        data['state_registration'] = '562547853'
        data['zipcode'] = '88963258'
        data['phone_number'] = '554855632685'
        data['owner'] = self.physical_person.cpf
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

    def test_goods_get_list(self):
        records = Good.objects.all()
        request = self.client.get('/v1/goods/')

        self.assertEquals(request.status_code, status.HTTP_200_OK)
        self.assertEquals(len(json.loads(request.content)), len(records))

    def test_goods_post(self):
        new_record = GoodSerializer({
            'good_type': 'imovel',
            'description': 'Some good description',
            'owner': self.physical_person.cpf
        }).data
        request = self.client.post(
            '/v1/goods/',
            json.dumps(new_record),
            content_type='application/json'
        )
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        good = Good.objects.get(description=new_record['description'])
        self.assertEquals(good.description, new_record['description'])

    def test_goods_post_invalid_owner(self):
        new_record = GoodSerializer({
            'good_type': 'empresa',
            'description': 'Some good description',
            'owner': '25632600014526'
        }).data
        request = self.client.post(
            '/v1/goods/',
            json.dumps(new_record),
            content_type='application/json'
        )
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_goods_post_invalid_type(self):
        new_record = GoodSerializer(baker.make(Good)).data
        new_record['good_type'] = 'carro'

        request = self.client.post(
            '/v1/goods/',
            json.dumps(new_record),
            content_type='application/json'
        )
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_goods_get(self):
        record = Good.objects.get(pk=1)
        request = self.client.get(f'/v1/goods/{record.id}/')
        data = json.loads(request.content)

        self.assertEquals(request.status_code, status.HTTP_200_OK)
        self.assertEquals(record.id, data['id'])
        self.assertEquals(record.good_type, data['good_type'])
        self.assertEquals(record.description, data['description'])
        self.assertEquals(record.owner, data['owner'])

    def test_goods_non_existent_id(self):
        request = self.client.get(f'/v1/goods/{999}/')
        self.assertEquals(request.status_code, 404)

    def test_goods_put(self):
        record = Good.objects.get(pk=1)
        data = GoodSerializer(record).data
        data['owner'] = self.physical_person.cpf
        request = self.client.put(
            f'/v1/goods/{data["id"]}/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        record = Good.objects.get(pk=1)
        self.assertEquals(record.owner, data['owner'])

    def test_goods_put_invalid_owner(self):
        record = Good.objects.get(pk=1)
        data = GoodSerializer(record).data
        data['owner'] = '111222333444555'
        request = self.client.put(
            f'/v1/goods/{data["id"]}/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_goods_delete(self):
        record = Good.objects.get(pk=1)
        request = self.client.delete(f'/v1/goods/{record.id}/')

        self.assertEquals(request.status_code, status.HTTP_200_OK)
        records = Good.objects.filter(pk=1)
        self.assertEquals(len(records), 0)
