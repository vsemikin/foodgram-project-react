from django_filters import FilterSet, filters

from .models import User
# from recipes.models import Recipe


class FollowFilter(FilterSet):
    """Model for filtering subscriptions."""
    recipes_limit = filters.NumberFilter(method="limit")

    def limit(self, queryset, name, value):
        """The method limits the number of recipes in the profile."""
        # recipes = Recipe.objects.all().filter(author=self.request.user)
        # return queryset.filter(following__recipes__in=recipes[:value])
        return queryset.recipes.all()[:value]

    class Meta:
        model = User
        fields = ["recipes_limit"]
