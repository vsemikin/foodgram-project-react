from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()
router.register("recipes", RecipeViewSet, basename="Recipe")
router.register("tags", TagViewSet, basename="Tag")
router.register("ingredients", IngredientViewSet, basename="Ingredient")

urlpatterns = [
    path("", include(router.urls)),
]
