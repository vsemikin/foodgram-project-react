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


# class IngredientAmountListSerializer(serializers.ListSerializer):
#     """."""
#     def create(self, validated_data):
#         ingredients = [IngredientAmount(**item) for item in validated_data]
#         return IngredientAmount.objects.bulk_create(ingredients)


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Serializer for the IngredientAmount model."""
    # name = serializers.CharField(
    #     source="ingredient.name",
    #     read_only=True,
    #     # many=True
    # )
    # measurement_unit = serializers.CharField(
    #     source="ingredient.measurement_unit",
    #     read_only=True,
    #     # many=True
    # )

    class Meta:
        # fields = ("id", "name", "measurement_unit", "amount")
        fields = ("id", "amount")
        model = IngredientAmount
        # list_serializer_class = IngredientAmountListSerializer


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the Tag model."""
    class Meta:
        fields = ("id", "name", "color", "slug")
        model = Tag


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the Recipe model."""
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(many=True)

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
        recipe = validated_data.pop("ingredients")
        ingredients = [
            Recipe.objects.create(ingredients=IngredientAmount(**item) for item in validated_data.pop("ingredients"))
        ]
        # IngredientAmount.objects.bulk_create(ingredients)
        return ingredients
        


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
