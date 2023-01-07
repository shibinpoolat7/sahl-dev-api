"""
Tests for rent APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Vehicle

from rent.serializers import (
    VehicleSerializer,
    VehicleDetailSerializer,
)


VEHICLES_URL = reverse('rent:vehicle-list')

def detail_url(vehicle_id):
    """Create and return a vehicle detail URL."""
    return reverse('rent:vehicle-detail', args=[vehicle_id])


def create_vehicle(user, **params):
    """Create and return a sample vehicle."""
    defaults = {
        'vehicle_type' : 'Sample vehicle type',
        'vehicle_name' : 'Sample vehicle name',
        'registration_no' : '234355',
        'daily_min_rate' : Decimal('10.00'),
        'daily_max_rate' : Decimal('10.00'),
        'monthly_min_rate' : Decimal('233.44'),
        'monthly_max_rate' : Decimal('1034.44'),
        'status' : 'Ready',
        
    }
    defaults.update(params)

    vehicle = Vehicle.objects.create(user=user, **defaults)
    return vehicle

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicVehicleAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(VEHICLES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateVehicleApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_vehicles(self):
        """Test retrieving a list of vehicles."""
        create_vehicle(user=self.user)
        create_vehicle(user=self.user)

        res = self.client.get(VEHICLES_URL)

        vehicles = Vehicle.objects.all().order_by('-id')
        serializer = VehicleSerializer(vehicles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_vehicle_list_limited_to_user(self):
        """Test list of vehicles is limited to authenticated user."""
        other_user = create_user(email='user1@example.com', password='test123')
        create_vehicle(user=other_user)
        create_vehicle(user=self.user)

        res = self.client.get(VEHICLES_URL)

        vehicles = Vehicle.objects.filter(user=self.user)
        serializer = VehicleSerializer(vehicles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_vehicle_detail(self):
        """Test get vehicle detail."""
        vehicle = create_vehicle(user=self.user)

        url = detail_url(vehicle.id)
        res = self.client.get(url)

        serializer = VehicleDetailSerializer(vehicle)
        self.assertEqual(res.data, serializer.data)

    def test_partial_update(self):
        """Test partial update of a vehicle."""
        vehicle_type = 'Sample Vehicle type'
        vehicle = create_vehicle(
            user=self.user,
            vehicle_name='Sample vehicle Name',
            vehicle_type=vehicle_type,
            registration_no='234355',
            daily_min_rate=Decimal('10.00'),
            daily_max_rate=Decimal('10.00'),
            monthly_min_rate=Decimal('233.44'),
            monthly_max_rate=Decimal('1034.44'),
            status='Ready',
        )

        payload = {'vehicle_name': 'New vehicle name'}
        url = detail_url(vehicle.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.vehicle_name, payload['vehicle_name'])
        self.assertEqual(vehicle.vehicle_type, vehicle_type)
        self.assertEqual(vehicle.user, self.user)

    def test_full_update(self):
        """Test full update of vehicle."""
        vehicle = create_vehicle(
            user=self.user,
            vehicle_name='Sample vehicle Name',
            vehicle_type='Sample vehicle type',
            registration_no='234355',
            daily_min_rate=Decimal('10.00'),
            daily_max_rate=Decimal('10.00'),
            monthly_min_rate=Decimal('233.44'),
            monthly_max_rate=Decimal('1034.44'),
            status='Ready',
        )

        payload = {
            'vehicle_name': 'New vehicle name',
            'vehicle_type': 'New vehicle type',
            'status': 'New',
            'registration_no': '67868687',
            'daily_min_rate': Decimal('2.50'),
            'daily_max_rate' : Decimal('10.00'),
            'monthly_min_rate' : Decimal('10.00'),
            'monthly_max_rate' : Decimal('10.00'),
        }
        url = detail_url(vehicle.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        vehicle.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(vehicle, k), v)
        self.assertEqual(vehicle.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the vehicle user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        vehicle = create_vehicle(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(vehicle.id)
        self.client.patch(url, payload)

        vehicle.refresh_from_db()
        self.assertEqual(vehicle.user, self.user)

    def test_delete_vehicle(self):
        """Test deleting a vehicle successful."""
        vehicle = create_vehicle(user=self.user)

        url = detail_url(vehicle.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vehicle.objects.filter(id=vehicle.id).exists())

    def test_vehicle_other_users_vehicle_error(self):
        """Test trying to delete another users vehicle gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        vehicle = create_vehicle(user=new_user)

        url = detail_url(vehicle.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Vehicle.objects.filter(id=vehicle.id).exists())
