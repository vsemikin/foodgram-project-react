from django.conf import settings
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import Ingredient, Favorite, Recipe, ShoppingCart, Tag
from .permissions import IsOwnerOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer)

User = settings.AUTH_USER_MODEL


class RecipeViewSet(viewsets.ModelViewSet):
    """The class returns all recipes or creates a new recipe or
    modifies a port."""
    queryset = Recipe.objects.all().order_by("-id")
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = [
        "get",
        "post",
        "put",
        "delete",
    ]

    def perform_create(self, serializer):
        """The function passes the current user as the author of the recipe
        published from his profile."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """The function passes the current user as the author of the recipe
        updated from his profile."""
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=["get", "delete"],
        permission_classes=(IsAuthenticated,),
        url_path="shopping_cart",
    )
    def shopping_cart(self, request, pk=None):
        """Function to add or remove a recipe in the shopping list."""
        recipe = self.get_object()
        if request.method == "GET":
            instance = ShoppingCart.objects.create(
                recipe=recipe,
                user=request.user
            )
            serializer = ShoppingCartSerializer(instance)
            return Response(serializer.data)
        else:
            instance = ShoppingCart.objects.filter(
                recipe=recipe,
                user=request.user
            )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["get", "delete"],
        url_path="favorite",
    )
    def favorite(self, request, pk=None):
        """Function to add or remove a recipe in the favorite list."""
        recipe = self.get_object()
        if request.method == "GET":
            instance = Favorite.objects.create(
                recipe=recipe,
                user=request.user
            )
            serializer = FavoriteSerializer(instance)
            return Response(serializer.data)
        else:
            instance = Favorite.objects.filter(
                recipe=recipe,
                user=request.user
            )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["get"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="download_shopping_cart",
    )
    def download_shopping_cart(self, request):
        """The function returns the shopping list in a file."""
        shopping_cart = {}
        recipes = ShoppingCart.objects.filter(user=request.user)
        for item in recipes:
            ingredients = item.recipe.ingredients.all().values()
            ingredients_amount = item.recipe.recipes_amount.all().values()
            for idx in range(len(ingredients)):
                name = ingredients[idx]["name"]
                amount = ingredients_amount[idx]["amount"]
                measurement_unit = ingredients[idx]["measurement_unit"]
                if f"{name}({measurement_unit})" in shopping_cart:
                    shopping_cart[f"{name}({measurement_unit})"] += amount
                else:
                    shopping_cart[f"{name}({measurement_unit})"] = amount
        response = HttpResponse(content_type='.txt')
        response.write(
            "\n".join(
                f"{key} — {value}" for key, value in shopping_cart.items()
            )
        )
        return response


class TagViewSet(viewsets.ModelViewSet):
    """The class returns all or one tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    http_method_names = ["get"]


class IngredientViewSet(viewsets.ModelViewSet):
    """The class return all or one Ingredient."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    http_method_names = ["get"]
