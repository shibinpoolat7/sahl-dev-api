"""
Views for the rent APIs
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Vehicle,Customer,Agreement
from rent import serializers

# @extend_schema_view(
#     list=extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 'tags',
#                 OpenApiTypes.STR,
#                 description='Comma separated list of tag IDs to filter',
#             ),
#             OpenApiParameter(
#                 'ingredients',
#                 OpenApiTypes.STR,
#                 description='Comma separated list of ingredient IDs to filter',
#             ),
#         ]
#     )
# )


class VehicleViewSet(viewsets.ModelViewSet):
    """View for manage vehicle APIs."""
    serializer_class = serializers.VehicleDetailSerializer
    queryset = Vehicle.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve Vehicles for authenticated user."""
        # tags = self.request.query_params.get('tags')
        # ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        # if tags:
        #     tag_ids = self._params_to_ints(tags)
        #     queryset = queryset.filter(tags__id__in=tag_ids)
        # if ingredients:
        #     ingredient_ids = self._params_to_ints(ingredients)
        #     queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.VehicleSerializer
        elif self.action == 'upload_image':
            return serializers.VehicleImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new vehicle."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to vehicle."""
        vehicle = self.get_object()
        serializer = self.get_serializer(vehicle, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerViewSet(viewsets.ModelViewSet):
    """View for manage customer APIs."""
    serializer_class = serializers.CustomerDetailSerializer
    queryset = Customer.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve Customers for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.CustomerSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new customer."""
        serializer.save(user=self.request.user)


class AgreementViewSet(viewsets.ModelViewSet):
    """View for manage Agreement APIs."""
    serializer_class = serializers.AgreementDetailSerializer
    queryset = Agreement.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve Agreements for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.AgreementSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Agreement."""
        serializer.save(user=self.request.user)
