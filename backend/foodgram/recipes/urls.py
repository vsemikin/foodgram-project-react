from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteViewSet, FollowViewSet, IngredientViewSet,
                    RecipeViewSet, ShoppingCartViewSet, TagViewSet)

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
    "users/subscriptions",
    FollowViewSet,
    basename="Follows"
)
router.register(
    r"users/(?P<user_id>\d+)/subscribe",
    FollowViewSet,
    basename="Follow"
)

urlpatterns = [
    path(
        "recipes/download_shopping_cart/",
        # ShoppingCartViewSet.as_view({"get": "list"}),
        ShoppingCartViewSet.as_view(),
        name="ShoppingCartDownload"
    ),
    path("", include(router.urls)),
    path("", include("users.urls")),
]
