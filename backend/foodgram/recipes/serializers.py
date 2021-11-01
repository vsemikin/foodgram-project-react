from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator
from users.serializers import UserSerializer

from .models import Favorite, Follow, Ingredient, IngredientAmount, Recipe, Tag
from users.models import User


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
    id = serializers.IntegerField()

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

    class Meta:
        fields = (
            "id",
            # "tags",
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
        ingredients = validated_data.pop("recipes_amount")
        recipe = Recipe.objects.create(**validated_data)
        for item in ingredients:
            current_ingredient = Ingredient(id=item["id"])
            IngredientAmount.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=item["amount"]
            )
        return recipe


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


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for the Follow model."""
    # email = serializers.EmailField(source="user.email", read_only=True)
    user = serializers.CharField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all()
    )

    class Meta:
        fields = ("user", "following")
        model = Follow
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Follow.objects.all(),
        #         fields=("user", "following"),
        #         message="The subscriber:blogger combination must be unique!"
        #     )
        # ]

    # def validate(self, data):
    #     """The function prohibits subscribing to yourself."""
    #     if data["following"] == self.context["request"].user:
    #         raise serializers.ValidationError(
    #             "It is impossible to subscribe to yourself"
    #         )
    #     return data
