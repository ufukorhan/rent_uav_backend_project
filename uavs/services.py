import datetime
from uavs.models import UAVCategory, UAV, RentedUAV
from users.models import User
from utils.interfaces import Service


class UAVCategoryService(Service):
    """
    Service class for managing UAVCategory objects.
    """

    def create_object(self, name: str, **fields) -> UAVCategory:
        """
        Creates a new UAVCategory object with the given name and fields.

        Args:
            name (str): The name of the new UAVCategory object.
            **fields: Additional fields to be set on the new UAVCategory object.

        Returns:
            UAVCategory: The newly created UAVCategory object.
        """
        return UAVCategory.objects.create(name=name, **fields)

    def update_object(self, instance: UAVCategory, **fields) -> UAVCategory:
        """
        Updates the given UAVCategory object with the given fields.

        Args:
            instance (UAVCategory): The UAVCategory object to update.
            **fields: The fields to update on the UAVCategory object.

        Returns:
            UAVCategory: The updated UAVCategory object.
        """
        for key, value in fields.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete_object(self, instance: UAVCategory) -> None:
        """
        Deletes the given UAVCategory object.

        Args:
            instance (UAVCategory): The UAVCategory object to delete.
        """
        instance.is_active = False
        instance.save()


class RentedUAVService(Service):
    """
    Service class for creating, updating and deleting RentedUAV objects.
    """

    def create_object(
        self,
        uav: UAV,
        user: User,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        **_,
    ) -> RentedUAV:
        return RentedUAV.objects.create(
            uav=uav, user=user, start_date=start_date, end_date=end_date
        )

    def update_object(self, instance: RentedUAV, **fields) -> RentedUAV:
        for key, value in fields.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete_object(self, instance: RentedUAV) -> None:
        instance.is_active = False
        instance.save()


class UAVService(Service):
    """
    A service class for managing UAV objects.

    This class provides methods for creating, updating, and deleting UAV objects,
    as well as renting UAVs and creating rented UAV objects.

    Attributes:
        rented_uav_service (RentedUAVService): A service object for managing rented UAVs.
    """

    rented_uav_service = RentedUAVService()

    def create_object(
        self,
        brand: str,
        model: str,
        weight: float,
        category: UAVCategory,
        is_rental: bool,
        **_,
    ) -> UAV:
        instance = UAV.objects.create(
            brand=brand,
            model=model,
            weight=weight,
            is_rental=is_rental,
        )
        instance.category.add(category)
        return instance

    def update_object(self, instance: UAV, **fields) -> UAV:
        for key, value in fields.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete_object(self, instance: UAV) -> None:
        instance.is_active = False
        instance.save()

    @classmethod
    def rent_uav(
        cls,
        uav: UAV,
        user: User,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> RentedUAV:
        if uav.is_rental:
            instance = cls.rented_uav_service.create_object(
                uav=uav,
                user=user,
                start_date=start_date,
                end_date=end_date,
            )
            uav.is_rental = False
            uav.save()
            return instance

        raise ValueError("The UAV is not rental")
