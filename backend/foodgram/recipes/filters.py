from django_filters import FilterSet, filters

from .models import Ingredient, Recipe


class IngredientFilter(FilterSet):
    """Model Filter Ingredient."""

    name = filters.CharFilter(field_name="name", lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ["name"]


class RecipeFilter(FilterSet):
    """Model Filter Ingredient."""

    author = filters.CharFilter(field_name="author__id", lookup_expr="exact")
    tags = filters.AllValuesMultipleFilter(
        field_name="tags__slug",
        lookup_expr="iexact",
    )
    is_favorited = filters.BooleanFilter(method="is_in_favorited")
    is_in_shopping_cart = filters.BooleanFilter(method="is_shopping_cart")

    def is_in_favorited(self, queryset, name, value):
        """The method returns recipes from the favorited current user."""
        if value is True:
            return queryset.filter(favorites_recipe__user=self.request.user)
        return queryset

    def is_shopping_cart(self, queryset, name, value):
        """The method returns recipes from the current user's shopping list."""
        if value is True:
            return queryset.filter(carts__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = [
            "author",
            "tags",
            "is_favorited",
            "is_in_shopping_cart",
        ]
