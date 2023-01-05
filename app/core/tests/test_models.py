"""
Tests for models.
"""
from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_vehicle(self):
        """Test creating a vehicle is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        vehicle = models.Vehicle.objects.create(
            user=user,
            vehicle_type='Sample vehicle type',
            vehicle_name='Sample vehicle name',
            registration_no='234355',
            daily_min_rate=Decimal('10.00'),
            daily_max_rate=Decimal('10.00'),
            monthly_min_rate=Decimal('10.00'),
            monthly_max_rate=Decimal('10.00'),
            status='Ready',
        )

        self.assertEqual(str(vehicle), vehicle.vehicle_name)

    @patch('core.models.uuid.uuid4')
    def test_vehicle_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.vehicle_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/vehicle/{uuid}.jpg')

    def test_create_customer(self):
        """Test creating a customer is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        customer = models.Customer.objects.create(
            user=user,
            customer_type='Sample customer type',
            customer_name='Sample customer name',
            cr_id_no='234355',
            customer_email='test@example.com',
            customer_mobile='23423233',
            customer_phone='343443',
            customer_address='test address',
            is_blocked=False,
        )

        self.assertEqual(str(customer), customer.customer_name)

    def test_create_agreement(self):
        """Test creating a agreement is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        customer = models.Agreement.objects.create(
            user=user,
            rent_type='Sample Rent Type',
            agreement_no='234',
            deposit_type='Cash',
            external_customer_name='',

            checkin_date='2022-12-12',
            checkout_date='',
            
            customer=models.Customer.objects.get(customer_email='test@example.com'),
            vehicle=models.Vehicle.objects.get(vehicle_name='Sample vehicle name'),
        )

        self.assertEqual(str(customer), customer.customer_name)
