from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSeializer):
    """Serializer for the User model."""
    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name"
            # "is_subscribed"
        )
