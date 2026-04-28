from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Recipe, Category, Ingredient
from .forms import RecipeForm, IngredientForm


def index(request):
    sort = request.GET.get("sort", "-created_at")
    recipes = Recipe.objects.select_related("category").all().order_by(sort)
    categories = Category.objects.all()
    return render(request, "recipes/index.html", {
        "recipes": recipes,
        "categories": categories,
        "current_sort": sort,
    })


def category_recipes(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    recipes = Recipe.objects.filter(category=category).select_related("category")
    return render(request, "recipes/category.html", {
        "category": category,
        "recipes": recipes,
    })


def search(request):
    q = request.GET.get("q", "")
    if q:
        results = Recipe.objects.filter(
            Q(title__icontains=q) |
            Q(author__icontains=q) |
            Q(category__name__icontains=q)
        ).select_related("category")
    else:
        results = Recipe.objects.none()
    return render(request, "recipes/search.html", {
        "results": results,
        "query": q,
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