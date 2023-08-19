from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
            "password",
        )
        read_only_fields = ("id", "is_staff", "is_active", "date_joined", "last_login")
        extra_kwargs = {
            'password': {'write_only': True}
        } 


class UserMeSerializer(serializers.ModelSerializer):
    class Meta(UserSerializer.Meta):
        fields = ("id", "email", "is_staff", "is_active", "date_joined", "last_login")
        read_only_fields = (
            "id",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
        )
