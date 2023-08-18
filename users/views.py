from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from uavs.models import RentedUAV
from uavs.serializers import RentedUAVSerializer
from users.models import User
from users.serializers import UserSerializer, UserMeSerializer
from users.services import UserService
from utils.permissions import IsSuperUser


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides CRUD operations for User objects.

    Attributes:
        queryset (QuerySet): The queryset of User objects to be used by the viewset.
        serializer_class (Serializer): The serializer class to be used by the viewset.
        service (UserService): An instance of the UserService class to handle business logic.
        permission_classes (list): The permission classes to be used by the viewset.

    Methods:
        perform_create(serializer): Overrides the default create behavior to use the UserService.
        perform_update(serializer): Overrides the default update behavior to use the UserService.
        me(request): A custom action that returns the authenticated user's data.
        rental_records(request): A custom action that returns the authenticated user's rental records.
    """
     
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    service = UserService()
    permission_classes = [IsAuthenticated, IsSuperUser]

    def perform_create(self, serializer):
        serializer.instance = self.service.create_object(**serializer.validated_data)

    def perform_update(self, serializer):
        self.service.update_object(serializer.instance, **serializer.validated_data)

    @action(
        detail=False,
        methods=["get"],
        serializer_class=UserMeSerializer,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """
        Returns the serialized data of the authenticated user.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object containing the serialized data of the authenticated user.
        """
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        serializer_class=RentedUAVSerializer,
        permission_classes=[IsAuthenticated],
        pagination_class=PageNumberPagination,
        url_path="me/rental-records",
    )
    def rental_records(self, request):
        """
        Retrieve a list of rented UAVs for the authenticated user.

        Args:
            request: The request object.

        Returns:
            A Response object containing a serialized list of rented UAVs.
        """
        rented_uav_list = RentedUAV.objects.filter(user=request.user)

        page = self.paginate_queryset(rented_uav_list)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(rented_uav_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
