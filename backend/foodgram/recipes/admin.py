from django.contrib import admin

from .models import Ingredient, Recipe, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """The class describes recipe model in the admin panel."""
    list_display = ("pk", "name", "author")
    list_filter = ("author", "name", "tags")


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """The class describes ingredient model in the admin panel."""
    list_display = ("pk", "name", "measurement_unit")
    list_filter = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """The class describes tag model in the admin panel."""
    list_display = ("pk", "name")
