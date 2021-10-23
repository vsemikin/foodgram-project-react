from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet

router = DefaultRouter()
router.register("recipes", RecipeViewSet, basename="Recipe")

urlpatterns = [
    path("v1/", include(router.urls)),
]
