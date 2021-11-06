from django.contrib import admin

from .inlines import IngredientAmountInline
from .models import Ingredient, IngredientAmount, Recipe, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """The class describes recipe model in the admin panel."""
    list_display = ("pk", "name", "author")
    readonly_fields = ('in_favorite',)
    inlines = [IngredientAmountInline]
    list_filter = ("author", "name", "tags")

    def in_favorite(self, instance):
        """."""
        return instance.favorites_recipe.all().count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """The class describes ingredient model in the admin panel."""
    list_display = ("pk", "name", "measurement_unit")
    list_filter = ("name",)


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    """The class describes ingredient model in the admin panel."""
    list_display = ("pk", "recipe", "ingredient", "amount")
    search_fields = ('recipe',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """The class describes tag model in the admin panel."""
    list_display = ("pk", "name")
    prepopulated_fields = {'slug': ('name',)}
