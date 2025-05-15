from rest_framework import serializers
from accounts.models import CustomeUser
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.shortcuts import get_object_or_404

class UserMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomeUser  
        fields = ['id', 'email']

class RegistrationSerializer(serializers.ModelSerializer):

    """
    Serializer for user registration.

    Fields:
        - email: User's email address.
        - password: Primary password.
        - password_confirm: Confirmation for the primary password (write-only).

    Validation:
        - Ensures both password fields match.
        - Validates password strength using Django's built-in password validator.

    On creation:
        - Removes 'password_confirm' from the validated data.
        - Creates a new user using the custom user model.
    """
    
    password_confirm = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = CustomeUser
        fields = ["email", "password", "password_confirm"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs.get("password") != attrs.get("password_confirm"):
            raise serializers.ValidationError({"detail": "Passwords do not match"})

        try:
            validate_password(attrs["password"])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"detail": list(e.messages)})

        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        return CustomeUser.objects.create_user(**validated_data)


class ResendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(label=("Email"), write_only=True)

    def validate(self, attrs):
        user = get_object_or_404(CustomeUser, email=attrs.get("email"))
        attrs["user"] = user
        return attrs