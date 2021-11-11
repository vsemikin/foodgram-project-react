from django_filters import FilterSet, filters

from .models import Follow


class FollowFilter(FilterSet):
    """Model for filtering subscriptions."""
    recipes_limit = filters.NumberFilter(method="limit")

    def limit(self, queryset, name, value):
        """The method limits the number of recipes in the profile."""
        return queryset.filter()

    class Meta:
        model = Follow
        fields = ["recipes_limit"]
