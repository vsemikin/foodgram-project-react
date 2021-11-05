from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.serializers import UserSerializer

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


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
            "cooking_time"
        )
        model = Recipe

    def to_representation(self, obj):
        """."""
        self.fields['tags'] = TagSerializer(many=True)
        return super().to_representation(obj)

    def get_is_in_shopping_cart(self, obj):
        """."""
        request = self.context.get("request")
        if ShoppingCart.objects.filter(recipe=obj, user=request.user).exists():
            return True
        return False

    def get_is_favorited(self, obj):
        """."""
        request = self.context.get("request")
        if Favorite.objects.filter(recipe=obj, user=request.user).exists():
            return True
        return False

    def create(self, validated_data):
        """Recipe creation."""
        ingredients_data = validated_data.pop("recipes_amount")
        tags_data = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        for item in ingredients_data:
            current_ingredient = Ingredient(id=item["ingredient"]["id"])
            IngredientAmount.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=item["amount"]
            )
        return recipe

    def update(self, instance, validated_data):
        """Recipe update."""
        ingredients_data = validated_data.pop("recipes_amount")
        ingredients = (instance.recipes_amount).all()
        ingredients = list(ingredients)
        tags_data = validated_data.pop("tags")
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.tags.clear()
        instance.tags.set(tags_data)
        instance.save()
        instance.ingredients.clear()
        for item in ingredients_data:
            current_ingredient = Ingredient(id=item["ingredient"]["id"])
            IngredientAmount.objects.create(
                ingredient=current_ingredient,
                recipe=instance,
                amount=item["amount"]
            )
        return instance


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
