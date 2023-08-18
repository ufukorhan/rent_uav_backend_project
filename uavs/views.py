from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from uavs.models import UAVCategory, UAV, RentedUAV
from uavs.serializers import (
    UAVCategorySerializer,
    UAVSerializer,
    RentedUAVSerializer,
    RentUAVSerializer,
)
from uavs.services import UAVService
from utils.permissions import IsSuperUser
from uavs.filters import UAVFilter


class UAVCategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing UAV categories.

    Allows authenticated superusers to view and edit UAV categories.
    """
    queryset = UAVCategory.objects.all()
    serializer_class = UAVCategorySerializer
    permission_classes = [IsAuthenticated, IsSuperUser]


class UAVViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations on UAV objects.

    Attributes:
        queryset: A queryset of all UAV objects.
        serializer_class: The serializer class used for serializing and deserializing UAV objects.
        permission_classes: A list of permission classes that the viewset requires.
        filter_backends: A list of filter backend classes that the viewset uses for filtering.
        search_fields: A list of fields that the viewset uses for searching.
        uav_service: An instance of the UAVService class.
    """

    queryset = UAV.objects.all()
    serializer_class = UAVSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["brand", "category__name"]
    filterset_class = UAVFilter

    uav_service = UAVService()

    def get_queryset(self):
        queryset = self.queryset.exclude(is_rental=False)
        search = self.request.query_params.get("search", None)
        if search is not None:
            queryset = queryset.prefetch_related("category")
        return queryset

        

    @action(
        detail=False,
        methods=["get"],
        url_path="rental",
        serializer_class=UAVSerializer,
        permission_classes=[IsAuthenticated],
    )
    def rental_uavs(self, request):
        """
        Returns a paginated list of rental UAVs filtered by is_rental=True.
        If a search query parameter is provided, the queryset is filtered by the search term and prefetches the category.
        """
        queryset = self.queryset.filter(is_rental=True)
        search = self.request.query_params.get("search", None)
        if search is not None:
            queryset = queryset.prefetch_related("category")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        url_path="rent",
        serializer_class=RentUAVSerializer,
        permission_classes=[IsAuthenticated],
    )
    def rent(self, request):
        """
        Rent a UAV for a specified time period.

        Parameters:
        request (Request): The request object containing the data to rent a UAV.

        Returns:
        Response: The response object containing the rented UAV data.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            uav = UAV.objects.get(id=serializer.validated_data.get("uav_id"))
            rented_uav = self.uav_service.rent_uav(
                uav=uav,
                user=request.user,
                start_date=serializer.validated_data.get("start_date"),
                end_date=serializer.validated_data.get("end_date"),
            )
            return Response(
                self.get_serializer(rented_uav).data, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RentedUAVViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing rented UAVs.

    Allows superusers to view, create, edit and delete rented UAVs.
    """
    queryset = RentedUAV.objects.all()
    serializer_class = RentedUAVSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]
