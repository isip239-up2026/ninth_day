from django.contrib import admin
from .models import Category, Recipe, Ingredient, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "icon", "name"]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display  = ["title", "category", "author", "cooking_time", "servings"]
    list_filter   = ["category"]
    search_fields = ["title", "author"]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name", "amount", "recipe"]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["recipe", "ip_address", "created_at"]
