from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Recipe, Category, Ingredient, Favorite
from .forms import RecipeForm, IngredientForm


def index(request):
    sort = request.GET.get("sort", "-created_at")
    recipes = Recipe.objects.select_related("category").prefetch_related("favorites").all().order_by(sort)
    categories = Category.objects.all()
    return render(request, "recipes/index.html", {
        "recipes": recipes,
        "categories": categories,
        "current_sort": sort,
    })


def category_recipes(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    recipes = Recipe.objects.filter(category=category).select_related("category").prefetch_related("favorites")
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
        ).select_related("category").prefetch_related("favorites")
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
    ip = request.META.get("REMOTE_ADDR", "127.0.0.1")
    is_favorite = recipe.favorites.filter(ip_address=ip).exists()
    favorites_count = recipe.favorites.count()
    return render(request, "recipes/recipe_detail.html", {
        "recipe": recipe,
        "ingredients": ingredients,
        "form": form,
        "is_favorite": is_favorite,
        "favorites_count": favorites_count,
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


def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ip = request.META.get("REMOTE_ADDR", "127.0.0.1")
    favorite = Favorite.objects.filter(recipe=recipe, ip_address=ip).first()
    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(recipe=recipe, ip_address=ip)
    return redirect("recipe_detail", recipe_id=recipe.id)


def favorites(request):
    ip = request.META.get("REMOTE_ADDR", "127.0.0.1")
    recipes = Recipe.objects.filter(favorites__ip_address=ip).select_related("category").prefetch_related("favorites")
    return render(request, "recipes/favorites.html", {"recipes": recipes})