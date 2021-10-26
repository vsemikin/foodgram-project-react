from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from .models import Favorite, Ingredient, Recipe, Tag
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    """The class returns all recipes or creates a new recipe or
    modifies a port."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        """The function passes the current user as the author of the recipe
        published from his profile."""
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """The class returns all or one tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """The class return all or one Ingredient."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class FavoriteViewSet(viewsets.ModelViewSet):
    """Class for adding a recipe to favorites."""
    serializer_class = FavoriteSerializer

    @action(methods=["get"], detail=False, serializer_class=RecipeSerializer)
    def get_queryset(self):
        """The function returns all favorite recipes for a given user."""
        return Favorite.objects.filter(user=self.request.user)

    def get_recipe(self):
        """The function returns the recipe by its ID."""
        recipe_id = self.kwargs["recipe_id"]
        return get_object_or_404(Recipe, id=recipe_id)

    @action(methods=["get"], detail=False)
    def perform_create(self, serializer):
        """The function creates an entry in the favorites for the current user and
        the selected recipe."""
        serializer.save(user=self.request.user, recipe=self.get_recipe())
