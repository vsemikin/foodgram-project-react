from django_filters import filters, FilterSet

from .models import Ingredient


class IngredientFilter(FilterSet):
    """Model Filter Ingredient."""
    name = filters.CharFilter(
        field_name="name",
        lookup_expr="istartswith"
    )

    class Meta:
        model = Ingredient
        fields = ("name",)
