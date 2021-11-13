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
        request = self.context.get("request")
        if request.user.is_anonymous or not Follow.objects.filter(
            following=obj, user=request.user
        ).exists():
            return False
        return True

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
    """."""
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
            "recipes_count"
        )
        read_only_fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name"
        )
        model = User

    def get_is_subscribed(self, obj):
        """The function returns the subscription status."""
        request = self.context.get("request")
        if Follow.objects.filter(following=obj, user=request.user).exists():
            return True
        return False

    def get_recipes(self, obj):
        """The function returns all the recipes of the blogger
        subscribed to."""
        query_params = self.context["request"].query_params
        queryset = Recipe.objects.filter(author=obj).order_by("-id")
        if query_params:
            value = int(query_params["recipes_limit"])
            queryset = queryset[:value]
        serializer = RecipeFollowSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        """The function returns the number of recipes of the blogger
        subscribed to."""
        return Recipe.objects.filter(author=obj).count()
