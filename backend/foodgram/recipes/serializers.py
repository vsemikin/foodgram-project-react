from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Favorite, Ingredient, Recipe, Tag


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the Recipe model."""
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    ingredients = serializers.SlugRelatedField(
        queryset=Ingredient.objects.all(),
        slug_field="name",
        many=True
    )

    class Meta:
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "image",
            "name",
            "text",
            "cooking_time"
        )
        model = Recipe

    def create(self, validated_data):
        """."""
        ingredients = validated_data["ingredients"]
        for item in ingredients:
            Ingredient(name=item)
        recipe = Recipe(**validated_data)
        recipe.save()
        return recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the Tag model."""
    class Meta:
        fields = ("id", "name", "color", "slug")
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for the Ingredient model."""
    class Meta:
        fields = ("id", "name", "measurement_unit")
        model = Ingredient


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for the Favorite model."""
    # image = Base64ImageField()
    # recipes = RecipeSerializer(read_only=True)

    class Meta:
        # fields = ("id", "name", "image", "cooking_time")
        # fields = ("recipes",)
        exclude = ("id", "recipe", "user")
        model = Favorite
        extra_kwargs = {
            'recipe': {'write_only': True},
            'user': {'write_only': True}
        }
