from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)
from users.serializers import UserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for the Ingredient model."""

    class Meta:
        fields = ("id", "name", "measurement_unit")
        model = Ingredient


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Serializer for the IngredientAmount model."""

    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )
    id = serializers.IntegerField(source="ingredient.id")

    class Meta:
        fields = ("id", "name", "measurement_unit", "amount")
        model = IngredientAmount


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the Tag model."""

    class Meta:
        fields = ("id", "name", "color", "slug")
        model = Tag


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the Recipe model."""

    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        source="recipes_amount",
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        model = Recipe

    def to_representation(self, obj):
        """The function converts tag id to tag serializer representation."""
        self.fields["tags"] = TagSerializer(many=True)
        return super().to_representation(obj)

    def get_is_in_shopping_cart(self, obj):
        """The function returns the status of the recipe
        in the shopping list."""
        request = self.context.get("request")
        return not request.user.is_anonymous and ShoppingCart.objects.filter(
            recipe=obj, user=request.user
        ).exists()

    def get_is_favorited(self, obj):
        """The function returns the status of the recipe in the favorites."""
        request = self.context.get("request")
        return not request.user.is_anonymous and Favorite.objects.filter(
            recipe=obj, user=request.user
        ).exists()

    def create_ingredient_amount(self, ingredients, recipe):
        """Method for creating a model object IngredientAmount."""
        for item in ingredients:
            current_ingredient = Ingredient(id=item["ingredient"]["id"])
            IngredientAmount.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=item["amount"]
            )

    def create(self, validated_data):
        """Recipe creation."""
        ingredients_data = validated_data.pop("recipes_amount")
        tags_data = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        recipe.recipes_tag.set(tags_data)
        self.create_ingredient_amount(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Recipe update."""
        ingredients_data = validated_data.pop("recipes_amount")
        tags_data = validated_data.pop("tags")
        instance = super(RecipeSerializer, self).update(
            instance, validated_data
        )
        instance.recipes_tag.clear()
        instance.recipes_tag.set(tags_data)
        instance.save()
        instance.recipes_ingredient.clear()
        self.create_ingredient_amount(ingredients_data, instance)
        return instance

    def validate_ingredients(self, data):
        """Method for checking duplicate ingredients."""
        ingredients = []
        for ingredient in data:
            if ingredient["ingredient"]["id"] in ingredients:
                raise serializers.ValidationError(
                    "Ingredients contain duplicates"
                )
            ingredients.append(ingredient["ingredient"]["id"])
        return data

    def validate_tags(self, data):
        """Method for checking duplicate tags."""
        tags = []
        for tag in data:
            if tag in tags:
                raise serializers.ValidationError(
                    "Tags contain duplicates"
                )
            tags.append(tag)
        return data

    def validate_cooking_time(self, data):
        """Method for checking the cooking time field."""
        if data < 1:
            raise serializers.ValidationError(
                "Cooking time cannot be less than 1"
            )
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Serializer for the ShoppingCart model."""

    id = serializers.ReadOnlyField(source="recipe.id")
    name = serializers.ReadOnlyField(source="recipe.name")
    image = Base64ImageField(source="recipe.image", read_only=True)
    cooking_time = serializers.ReadOnlyField(source="recipe.cooking_time")

    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        model = ShoppingCart


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for the Favorite model."""

    id = serializers.ReadOnlyField(source="recipe.id")
    name = serializers.ReadOnlyField(source="recipe.name")
    image = Base64ImageField(source="recipe.image", read_only=True)
    cooking_time = serializers.ReadOnlyField(source="recipe.cooking_time")

    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        model = Favorite
