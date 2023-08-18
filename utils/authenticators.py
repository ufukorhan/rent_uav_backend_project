from typing import Union
from rest_framework.authtoken.models import Token
from users.models import User


class UAVAuthenticator:
    """
    Authenticator class for UAV users.

    This class provides methods to authenticate UAV users with their email and password.
    """

    def authenticate_with_credentials(
        self, email: str, password: str
    ) -> Union[str, None]:
        """
        Authenticates a user with the given email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            str: The authentication token if the user is authenticated successfully.
            None: If the user is not found or the password is incorrect.
        """
        try:
            user: User = User.objects.get(email=email)
            if user.password == password and user.is_active:
                token, _ = Token.objects.get_or_create(user=user)
                return token.key
        except User.DoesNotExist:
            return None
        
