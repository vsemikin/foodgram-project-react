from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
# from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from .filters import IngredientFilter
from .models import Ingredient, Recipe, Tag
from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, RecipeSerializer,
                          TagSerializer)

User = settings.AUTH_USER_MODEL


class RecipeViewSet(viewsets.ModelViewSet):
    """The class returns all recipes or creates a new recipe or
    modifies a port."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        """The function passes the current user as the author of the recipe
        published from his profile."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """."""
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    """The class returns all or one tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    """The class return all or one Ingredient."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class FavoriteViewSet(viewsets.ModelViewSet):
    """Class for adding a recipe to favorites."""
    serializer_class = FavoriteSerializer

    # @action(methods=["get"], detail=False, serializer_class=RecipeSerializer)
    # def get_queryset(self):
    #     """The function returns all favorite recipes for a given user."""
    #     return Favorite.objects.filter(user=self.request.user)

    def get_recipe(self):
        """The function returns the recipe by its ID."""
        recipe_id = self.kwargs["recipe_id"]
        return get_object_or_404(Recipe, id=recipe_id)

    # @action(methods=["get"], detail=False)
    def perform_create(self, serializer):
        """The function creates an entry in the favorites for the current user and
        the selected recipe."""
        serializer.save(user=self.request.user, recipe=self.get_recipe())

    # def perform_destroy(self, instance):
    #     """The function removes a recipe from favorites."""
    #     favorite = get_object_or_404(
    #         user=self.request.user, recipe=self.get_recipe()
    #     )
    #     favorite.delete()

    def perform_destroy(self, instance):
        """."""
        instance.delete()


class FollowViewSet(viewsets.ModelViewSet):
    """The class returns a list of all subscribers and
    creates a subscription."""
    serializer_class = FollowSerializer
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ("=user__username", "=following__username")

    def get_queryset(self):
        """The function returns a queryset containing all subscribers
        of the current user."""
        return self.request.user.following.all()

    def get_user(self):
        """The function returns the recipe by its ID."""
        user_id = self.kwargs["user_id"]
        return get_object_or_404(User, id=user_id)

    def perform_create(self, serializer):
        """The function passes the current user as a subscriber to the
        specified blogger."""
        serializer.save(user=self.request.user, following=self.get_user())
