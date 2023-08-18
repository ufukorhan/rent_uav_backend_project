from users.models import User
from utils.interfaces import Service


class UserService(Service):
    """
    A service class for User model that provides methods for creating, updating and deleting User objects.
    """
    def create_object(self, email: str, password: str) -> User:
        """
        Creates a new User object with the given email.

        Args:
            email (str): The email of the user to be created.

        Returns:
            User: The newly created User object.
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            instance: User = User.objects.create(email=email, password=password)
            return instance

    def update_object(self, instance: User, **fields) -> User:
        """
        Updates the given User object with the given fields.

        Args:
            instance (User): The User object to be updated.
            **fields: The fields to be updated.

        Returns:
            User: The updated User object.
        """
        
        for key, value in fields.items():
            setattr(instance, key, value)
            instance.save()
        return instance

    def delete_object(self, instance: User) -> None:
        """
        Sof Deletes the given User object.

        Args:
            instance (User): The User object to be deleted.

        Returns:
            None
        """
        instance.is_active = False
        instance.save()
