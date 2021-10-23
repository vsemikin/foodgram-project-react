from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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


class Tag(models.Model):
    """The model describes the tags for fetching by recipes."""
    name = models.CharField("Название", max_length=100)
    color = ColorField("Цвет", format="hexa")
    slug = models.SlugField("Ярлык", unique=True)


class Ingredient(models.Model):
    """The model describes the recipe ingredient."""
    name = models.CharField("Название", max_length=100)
    measurement_unit = models.CharField("Единицы измерения", max_length=10)
