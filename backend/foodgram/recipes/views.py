from .serializers import RecipeSerializer
from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .models import Recipe

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    """The class returns all recipes or creates a new recipe or
    modifies a port."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
