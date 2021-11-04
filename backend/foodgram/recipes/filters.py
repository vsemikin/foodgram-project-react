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
    # is_in_shopping_cart = filters.BooleanFilter(
    #     method='filter_is_in_shopping_cart',
    #     lookup_expr="exact"
    # )

    class Meta:
        model = Recipe
        fields = [
            "author",
            "tags",
            # "is_in_shopping_cart",
        ]

    # def filter_is_in_shopping_cart(self, queryset, name, value):
    #     return queryset.filter(**{"is_in_shopping_cart": False})
