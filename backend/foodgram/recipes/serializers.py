from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator
from users.serializers import UserSerializer

from .models import Favorite, Follow, Ingredient, Recipe, Tag
from users.models import User


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

    # def create(self, validated_data):
    #     """."""
    #     ingredients = self.context["request"].data["ingredients"]
    #     for item in ingredients:
    #         Ingredient.objects.create(name=item)
    #     recipe = Recipe.objects.create(**validated_data)
    #     recipe.save()
    #     return recipe


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
