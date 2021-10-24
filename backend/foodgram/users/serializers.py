from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password"
            # "is_subscribed"
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Function for hashing the user's password."""
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
