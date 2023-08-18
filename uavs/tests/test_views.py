from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from ..models import UAV, UAVCategory, RentedUAV
from model_mommy import mommy
from datetime import datetime, timedelta


class UAVCategoryViewSetTestCase(APITestCase):
    BASE_URL = "/api/v1/uav-categories/"
    BASE_URL_DETAILED = "/api/v1/uav-categories/{}/"

    def setUp(self):
        user = User.objects.create_superuser(
            email='testuser@gmail.com',
            password='testpass'
        )
        self.client.force_authenticate(user=user)
        self.uav_category = UAVCategory.objects.create(name='Category 1')
        self.valid_payload = {'name': 'Category 2'}
        self.invalid_payload = {'name': ''}
    
    def tearDown(self) -> None:
        UAVCategory.objects.all().delete()


    def test_create_valid_uav_category(self):
        response = self.client.post(self.BASE_URL, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UAVCategory.objects.count(), 2)

    def test_create_invalid_uav_category(self):
        response = self.client.post(self.BASE_URL, data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UAVCategory.objects.count(), 1)

    def test_retrieve_uav_category(self):
        response = self.client.get(self.BASE_URL_DETAILED.format(self.uav_category.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'Category 1')

    def test_update_uav_category(self):
        response = self.client.put(self.BASE_URL_DETAILED.format(self.uav_category.id), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UAVCategory.objects.get(id=self.uav_category.id).name, 'Category 2')

    def test_delete_uav_category(self):
        response = self.client.delete(self.BASE_URL_DETAILED.format(self.uav_category.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UAVCategory.objects.count(), 0)

    def test_list_uav_categories(self):
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('count'), 1)


class UAVViewSetTestCase(APITestCase):
    BASE_URL = "/api/v1/uavs/"
    BASE_URL_DETAILED = "/api/v1/uavs/{}/"
    UAV_RENT_URL = "/api/v1/uavs/rent/"

    def setUp(self):
        self.user = User.objects.create_superuser(
            email='testuser@gmail.com',
            password='testpass'
            )
        self.client.force_authenticate(user=self.user)
        self.uav_category = mommy.make(UAVCategory)
        self.uav = mommy.make(UAV, category=[self.uav_category], brand='UAV 1')
        self.valid_payload = {'brand': 'UAV 2', 'category': self.uav_category.id, 'weight': 1.0, 'is_rental': True, 'model': 'Model 1'}
        self.invalid_payload = {'brand': '', 'category': self.uav_category.id}
        self.rented_uav = RentedUAV.objects.create(
            uav=self.uav,
            user=self.user,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
        )

    def test_list_uavs(self):
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('count'), 1)

    def test_create_valid_uav(self):
        response = self.client.post(self.BASE_URL, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UAV.objects.count(), 2)

    def test_create_invalid_uav(self):
        response = self.client.post(self.BASE_URL, data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UAV.objects.count(), 1)

    def test_retrieve_uav(self):
        response = self.client.get(self.BASE_URL_DETAILED.format(self.uav.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['brand'], 'UAV 1')

    def test_update_uav(self):
        response = self.client.put(self.BASE_URL_DETAILED.format(self.uav.id), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UAV.objects.get(id=self.uav.id).brand, 'UAV 2')

    def test_delete_uav(self):
        response = self.client.delete(self.BASE_URL_DETAILED.format(self.uav.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UAV.objects.count(), 0)

    # action endpoints tests

    def test_rent_invalid_date(self):
        data = {
            "uav_id": self.uav.id,
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        }
        response = self.client.post(self.UAV_RENT_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["end_date"],
            ['The end date cannot be before the current date'],
        )

    def test_rent_invalid_uav(self):
        data = {
            "uav_id": "invalid_id",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        }
        response = self.client.post(self.UAV_RENT_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "['“invalid_id” is not a valid UUID.']"
        )

    def test_rent(self):
        data = {
            "uav_id": self.uav.id,
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        }
        response = self.client.post(self.UAV_RENT_URL, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["uav_id"], str(self.uav.id))
        self.assertEqual(
            response.data["start_date"], data["start_date"]
        )
        self.assertEqual(
            response.data["end_date"], data["end_date"]
        )

        
class RentedUAVViewSetTestCase(APITestCase):
    BASE_URL = "/api/v1/rented-uavs/"
    BASE_URL_DETAILED = "/api/v1/rented-uavs/{}/"

    def setUp(self):
        self.user = User.objects.create_superuser(
            email='testuser@gmail.com',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)
        self.uav_category = mommy.make(UAVCategory)
        self.uav = mommy.make(UAV, category=[self.uav_category], brand='UAV 1')
        self.rented_uav = RentedUAV.objects.create(
            uav=self.uav,
            user=self.user,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
        )

    def test_rental_uavs(self):
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)


    def test_rented_uav_list(self):
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RentedUAV.objects.count(), 1)
        self.assertEqual(response.json()['results'][0]["id"], str(self.rented_uav.id))

    def test_rented_uav_detail(self):
        url = self.BASE_URL_DETAILED.format(self.rented_uav.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.rented_uav.id))

    def test_rented_uav_create(self):
        uav_id = mommy.make(UAV, category=[self.uav_category]).id
        data = {
            "uav": uav_id,
            "user": self.user.id,
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        }
        response = self.client.post(self.BASE_URL, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["uav"], uav_id)
        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(
            response.data["start_date"], data["start_date"]
        )
        self.assertEqual(
            response.data["end_date"], data["end_date"]
        )

    def test_rented_uav_update(self):
        url = self.BASE_URL_DETAILED.format(self.rented_uav.id)
        uav_id = mommy.make(UAV, category=[self.uav_category]).id
        data = {
            "uav": uav_id,
            "user": self.user.id,
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        }
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uav"], uav_id)
        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(
            response.data["start_date"], data["start_date"]
        )
        self.assertEqual(
            response.data["end_date"], data["end_date"]
        )

    def test_rented_uav_delete(self):
        url = self.BASE_URL_DETAILED.format(self.rented_uav.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
