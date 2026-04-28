from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Category, Ingredient
from .forms import RecipeForm, IngredientForm


def index(request):
    recipes = Recipe.objects.select_related("category").all()
    categories = Category.objects.all()
    return render(request, "recipes/index.html", {
        "recipes": recipes,
        "categories": categories,
    })


def category_recipes(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    recipes = Recipe.objects.filter(category=category).select_related("category")
    return render(request, "recipes/category.html", {
        "category": category,
        "recipes": recipes,
    })


def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()
            return redirect("recipe_detail", recipe_id=recipe.id)
    else:
        form = RecipeForm()
    return render(request, "recipes/add_recipe.html", {"form": form})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = recipe.ingredients.all()
    form = IngredientForm()
    return render(request, "recipes/recipe_detail.html", {
        "recipe": recipe,
        "ingredients": ingredients,
        "form": form,
    })


def add_ingredient(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()
    return redirect("recipe_detail", recipe_id=recipe.id)