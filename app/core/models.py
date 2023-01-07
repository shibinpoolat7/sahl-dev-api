"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

def vehicle_image_file_path(instance, filename):
    """Generate file path for new vehicle image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'vehicle', filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'


class Vehicle(models.Model):
    """Vehicle object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
    )
    vehicle_type = models.CharField(max_length=40)
    vehicle_name = models.CharField(max_length=255)
    registration_no = models.CharField(max_length=20)
    daily_min_rate = models.DecimalField(max_digits=10, decimal_places=3)
    daily_max_rate = models.DecimalField(max_digits=10, decimal_places=3)
    monthly_min_rate = models.DecimalField(max_digits=10, decimal_places=3)
    monthly_max_rate = models.DecimalField(max_digits=10, decimal_places=3)
    status = models.CharField(max_length=40)
    image = models.ImageField(null=True, upload_to=vehicle_image_file_path)

    def __str__(self):
        return self.vehicle_name


class Customer(models.Model):
    """Customer object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
    )
    customer_type = models.CharField(max_length=40)
    customer_name = models.CharField(max_length=255)
    cr_id_no = models.CharField(max_length=40)
    customer_email = models.EmailField(max_length=100)
    customer_mobile = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=100,null=True, default=None, blank=True)
    customer_address = models.TextField(null=True, default=None, blank=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_name


class Agreement(models.Model):
    """Agreement object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
    )
    rent_type = models.CharField(max_length=50)
    agreement_no = models.CharField(max_length=255)
    deposit_type = models.CharField(max_length=40)
    external_customer_name = models.EmailField(max_length=255,null=True, default=None, blank=True)

    checkin_date = models.DateField()
    checkout_date = models.DateField(null=True, default=None, blank=True)
    
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT, related_name="agreement_customer")
    vehicle = models.ForeignKey(Vehicle,on_delete=models.PROTECT, related_name="agreement_vehicle")


    def __str__(self):
        return self.customer_name
