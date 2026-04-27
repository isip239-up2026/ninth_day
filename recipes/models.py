from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    icon = models.CharField(max_length=10, default="🍽️", verbose_name="Иконка")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title        = models.CharField(max_length=200, verbose_name="Название")
    description  = models.TextField(verbose_name="Описание")
    category     = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                     null=True, related_name="recipes",
                                     verbose_name="Категория")
    author       = models.CharField(max_length=100, verbose_name="Автор")
    cooking_time = models.IntegerField(verbose_name="Время приготовления (мин)")
    servings     = models.IntegerField(default=4, verbose_name="Порций")
    image_url    = models.URLField(blank=True, verbose_name="Фото блюда")
    created_at   = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name="ingredients", verbose_name="Рецепт")
    name   = models.CharField(max_length=200, verbose_name="Название")
    amount = models.CharField(max_length=100, verbose_name="Количество")

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.name} — {self.amount}"


class Favorite(models.Model):
    recipe     = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                                   related_name="favorites", verbose_name="Рецепт")
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        unique_together = ["recipe", "ip_address"]

    def __str__(self):
        return f"{self.ip_address} → {self.recipe.title}"
