from django.contrib import admin

from .models import IngredientAmount


class IngredientAmountInline(admin.TabularInline):
    """."""
    model = IngredientAmount
