from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="user with this email already exists",
            )
        ]
    )

    def create(self, validated_data):
        if "is_employee" in validated_data and validated_data["is_employee"] is True:
            return User.objects.create_superuser(**validated_data)
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "blocked_until",
            "is_employee",
        ]
        # read_only_fields = ["blocked_until"]
        extra_kwargs = {"password": {"write_only": True}}
