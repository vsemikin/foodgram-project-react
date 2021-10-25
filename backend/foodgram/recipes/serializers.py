from rest_framework import serializers

from .models import Ingredient, Recipe, Tag


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the Recipe model."""
    class Meta:
        fields = (
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time"
        )
        model = Recipe


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
