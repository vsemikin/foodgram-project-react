from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.html import format_html

User = settings.AUTH_USER_MODEL


class Recipe(models.Model):
    """The model describes recipes published by the user."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор публикации"
    )
    name = models.CharField("Название", max_length=200)
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
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(limit_value=1, message="Time smaller 1")
        ],
        verbose_name="Время приготовления"
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class Tag(models.Model):
    """The model describes the tags for fetching by recipes."""
    name = models.CharField("Название", max_length=200)
    color = models.CharField(
        "Цвет", max_length=7,
        blank=True,
        null=True
    )
    slug = models.SlugField(
        "Ярлык", unique=True,
        max_length=200,
        blank=True,
        null=True
    )

    def colored_name(self):
        """Color in format HEX."""
        return format_html(
            '<span style="color: #{};">{}</span>',
            self.color,
        )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """The model describes the recipe ingredient."""
    name = models.CharField("Название", max_length=200)
    measurement_unit = models.CharField("Единицы измерения", max_length=200)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Favorite(models.Model):
    """The model describes the user's favorites section."""
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name="favorites_recipe",
        verbose_name=" Рецепт"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="favorites_user",
        verbose_name="Автор публикации"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "user"],
                name="unique_pair"
            ),
        ]
        verbose_name = "Избранное"
