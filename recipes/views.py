from django.shortcuts import render, get_object_or_404
from .models import Recipe, Category


def index(request):
    recipes = Recipe.objects.select_related("category").all()
    return render(request, "recipes/index.html", {"recipes": recipes})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, "recipes/recipe_detail.html", {"recipe": recipe})
