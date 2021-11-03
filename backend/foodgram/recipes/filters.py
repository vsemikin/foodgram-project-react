from django_filters import filters, FilterSet

from .models import Ingredient, Recipe


class IngredientFilter(FilterSet):
    """Model Filter Ingredient."""
    name = filters.CharFilter(
        field_name="name",
        lookup_expr="istartswith"
    )

    class Meta:
        model = Ingredient
        fields = ["name"]


class RecipeFilter(FilterSet):
    """Model Filter Ingredient."""
    author = filters.CharFilter(
        field_name="author__id",
        lookup_expr="exact"
    )
    tags = filters.AllValuesMultipleFilter(
        field_name="tags__slug",
        lookup_expr="iexact",
    )

    class Meta:
        model = Recipe
        fields = ["author", "tags"]
