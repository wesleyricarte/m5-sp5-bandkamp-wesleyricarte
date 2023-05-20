from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> User:
        return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.password = validated_data.get("password")
        if instance.password:
            instance.set_password(instance.password)

        instance.save()

        return instance

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_superuser",
        ]
        read_only_fields = ("is_superuser",)
        extra_kwargs = {
            "username": {"validators": [UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that username already exists.",
            )]},
            "email": {"validators": [UniqueValidator(
                queryset=User.objects.all()
            )]},
            "password": {"write_only": True},
        }
