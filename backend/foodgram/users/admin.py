from django.contrib import admin

from .models import User


@admin.register(User)
class RecipeAdmin(admin.ModelAdmin):
    """The class describes recipe model in the admin panel."""
    list_display = ("pk", "email", "username")
    list_filter = ("email", "username")
