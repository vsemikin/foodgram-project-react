from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe
from rest_framework import serializers

from .models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_subscribed"
        )
        extra_kwargs = {'password': {'write_only': True}}

    def get_is_subscribed(self, obj):
        """The function returns the subscription status."""
        current_user = self.context["request"].user
        if Follow.objects.filter(following=obj, user=current_user).exists():
            return True
        return False

    def create(self, validated_data):
        """Function for hashing the user's password."""
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class RecipeFollowSerializer(serializers.ModelSerializer):
    """Serializer for recipes in follow serializer."""
    name = serializers.ReadOnlyField()
    image = Base64ImageField(read_only=True)
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        model = Recipe


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for the Follow model."""
    email = serializers.ReadOnlyField(source="following.email")
    id = serializers.ReadOnlyField(source="following.id")
    username = serializers.ReadOnlyField(source="following.username")
    first_name = serializers.ReadOnlyField(source="following.first_name")
    last_name = serializers.ReadOnlyField(source="following.last_name")
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        model = Follow

    def get_is_subscribed(self, obj):
        """The function returns the subscription status."""
        if Follow.objects.filter(
            following=obj.following, user=obj.user
        ).exists():
            return True
        return False

    def get_recipes(self, obj):
        """The function returns all the recipes of the blogger
        subscribed to."""
        queryset = Recipe.objects.filter(author=obj.following)
        serializer = RecipeFollowSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        """The function returns the number of recipes of the blogger
        subscribed to."""
        return Recipe.objects.filter(author=obj.following).count()

    def validate(self, data):
        """The function prohibits subscribing to yourself."""
        if data["following"] == self.context["request"].user:
            raise serializers.ValidationError(
                "It is impossible to subscribe to yourself"
            )
        return data
