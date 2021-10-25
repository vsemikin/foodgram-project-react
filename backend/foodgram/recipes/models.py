from colorfield.fields import ColorField
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Recipe(models.Model):
    """The model describes recipes published by the user."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор публикации"
    )
    name = models.CharField("Название", max_length=100)
    image = models.ImageField("Картинка", upload_to="recipes/")
    text = models.TextField("Текстовое описание")
    tags = models.ManyToManyField(
        "Tag", related_name="tags",
        verbose_name="Теги"
    )
    ingredients = models.ManyToManyField(
        "Ingredient", related_name="ingredients",
        verbose_name="Ингридиенты"
    )
    cooking_time = models.TimeField("Время приготовления")

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class Tag(models.Model):
    """The model describes the tags for fetching by recipes."""
    name = models.CharField("Название", max_length=200)
    color = ColorField(
        "Цвет", format="hexa",
        max_length=7,
        blank=True,
        null=True
    )
    slug = models.SlugField(
        "Ярлык", unique=True,
        max_length=200,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Ingredient(models.Model):
    """The model describes the recipe ingredient."""
    name = models.CharField("Название", max_length=200)
    measurement_unit = models.CharField("Единицы измерения", max_length=200)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
