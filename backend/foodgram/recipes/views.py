from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer
from rest_framework import viewsets

from .models import Ingredient, Recipe, Tag


class RecipeViewSet(viewsets.ModelViewSet):
    """The class returns all recipes or creates a new recipe or
    modifies a port."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


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
