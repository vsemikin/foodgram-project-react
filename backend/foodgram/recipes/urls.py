from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteViewSet, FollowViewSet, IngredientViewSet,
                    RecipeViewSet, TagViewSet)

router = DefaultRouter()
router.register("recipes", RecipeViewSet, basename="Recipe")
router.register("tags", TagViewSet, basename="Tag")
router.register("ingredients", IngredientViewSet, basename="Ingredient")
router.register(
    r"recipes/(?P<recipe_id>\d+)/favorite",
    FavoriteViewSet,
    basename="Favorite"
)
router.register(
    r"users/(?P<user_id>\d+)/subscribe",
    FollowViewSet,
    basename="Follow"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include("users.urls")),
]
