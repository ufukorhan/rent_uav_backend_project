from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from uavs.models import UAVCategory, UAV, RentedUAV
from users.models import User
from uavs.services import UAVCategoryService, UAVService, RentedUAVService


class UAVCategoryServiceTestCase(TestCase):
    def setUp(self):
        self.service = UAVCategoryService()

    def test_create_object(self):
        category = self.service.create_object(name="Test Category")
        self.assertIsInstance(category, UAVCategory)

    def test_update_object(self):
        category = self.service.create_object(name="Test Category")
        updated_category = self.service.update_object(category, name="Updated Category")
        self.assertEqual(updated_category.name, "Updated Category")

    def test_delete_object(self):
        category = self.service.create_object(name="Test Category")
        self.service.delete_object(category)
        db_category = UAVCategory.objects.get(pk=category.pk)
        self.assertFalse(db_category.is_active)


class UAVServiceTestCase(TestCase):
    def setUp(self):
        self.category = UAVCategory.objects.create(name="Test Category")
        self.service = UAVService()

    def test_create_object(self):
        uav = self.service.create_object(
            brand="Test Brand",
            model="Test Model",
            weight=1.0,
            category=self.category,
            is_rental=True,
        )
        self.assertIsInstance(uav, UAV)

    def test_update_object(self):
        uav = self.service.create_object(
            brand="Test Brand",
            model="Test Model",
            weight=1.0,
            category=self.category,
            is_rental=True,
        )
        updated_uav = self.service.update_object(uav, brand="Updated Brand")
        self.assertEqual(updated_uav.brand, "Updated Brand")

    def test_delete_object(self):
        uav = self.service.create_object(
            brand="Test Brand",
            model="Test Model",
            weight=1.0,
            category=self.category,
            is_rental=True,
        )
        self.service.delete_object(uav)
        db_uav = UAV.objects.get(pk=uav.pk)
        self.assertFalse(db_uav.is_active)


class UAVRentedServiceTestCase(TestCase):
    def setUp(self):
        self.category = UAVCategory.objects.create(name="Test Category")
        self.uav = UAV.objects.create(
            brand="Test Brand",
            model="Test Model",
            weight=1.0,
            is_rental=True,
        )
        self.uav.category.add(self.category)
        self.uav.save()
        self.user = User.objects.create(email="testuser@testmail.com")
        self.start_date = timezone.now()
        self.end_date = self.start_date + timedelta(days=1)
        self.service = RentedUAVService()

    def test_create_object(self):
        rented_uav = self.service.create_object(
            uav=self.uav,
            user=self.user,
            start_date=self.start_date,
            end_date=self.end_date,
        )
        self.assertIsInstance(rented_uav, RentedUAV)

    def test_update_object(self):
        rented_uav = self.service.create_object(
            uav=self.uav,
            user=self.user,
            start_date=self.start_date,
            end_date=self.end_date,
        )
        updated_rented_uav = self.service.update_object(
            rented_uav, start_date=self.start_date + timedelta(days=2)
        )
        self.assertEqual(
            updated_rented_uav.start_date, self.start_date + timedelta(days=2)
        )

    def test_delete_object(self):
        rented_uav = self.service.create_object(
            uav=self.uav,
            user=self.user,
            start_date=self.start_date,
            end_date=self.end_date,
        )
        self.service.delete_object(rented_uav)
        db_rented_uav = RentedUAV.objects.get(pk=rented_uav.pk)
        self.assertFalse(db_rented_uav.is_active)
