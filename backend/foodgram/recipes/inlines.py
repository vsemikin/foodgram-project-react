from django.contrib import admin

from .models import IngredientAmount


class IngredientAmountInline(admin.TabularInline):
    """Model for interacting with ingredients in the admin panel."""
    model = IngredientAmount
