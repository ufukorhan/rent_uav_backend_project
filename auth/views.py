from urllib.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from auth.serializers import LoginSerializer
from utils.authenticators import UAVAuthenticator


class AuthView(APIView):
    permission_classes = []
    authenticator = UAVAuthenticator()
    serializer_class = LoginSerializer

    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = self.authenticator.authenticate_with_credentials(
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
            )
            if token:
                return Response({"token": token}, status=status.HTTP_200_OK)

            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
