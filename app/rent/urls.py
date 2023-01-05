"""
URL mappings for the rent app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from rent import views


router = DefaultRouter()
router.register('vehicles', views.VehicleViewSet)
router.register('customers', views.CustomerViewSet)
router.register('agreement', views.AgreementViewSet)

app_name = 'rent'

urlpatterns = [
    path('', include(router.urls)),
]
