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
    # is_favorited = filters.BooleanFilter(method="filter_is_favorited")
    # is_in_shopping_cart = filters.CharFilter(
    #     field_name="is_in_shopping_cart",
    #     lookup_expr="iexact"
    # )

    class Meta:
        model = Recipe
        fields = [
            "author",
            "tags",
            # "is_favorited",
            # "is_in_shopping_cart",
        ]

    # def filter_is_favorited(self, queryset, value):
    #     """."""
    #     request = self.context.get("request")
    #     # if value is not None:
    #     #     queryset = queryset.filter()
    #     return request
