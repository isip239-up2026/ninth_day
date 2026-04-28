from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Category, Ingredient
from .forms import RecipeForm, IngredientForm
from django.db.models import Q
from django.core.paginator import Paginator

def index(request):
    sort_field = request.GET.get('sort', '-created_at')
    recipe_list = Recipe.objects.all().order_by(sort_field)
    paginator = Paginator(recipe_list, 10)  # 10 рецептов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    recipes = Recipe.objects.select_related("category").all()
    return render(request, "recipes/index.html", {"recipes": recipes, 'page_obj': page_obj})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, "recipes/recipe_detail.html", {"recipe": recipe,
                                                          "ingr": recipe.ingredients.all(),
                                                          "ingredients_form": IngredientForm()})

def category_recipes(request, category_id):
    category1 = get_object_or_404(Category, id=category_id)
    return render(request, "recipes/category.html", {"recipe": Recipe.objects.filter(category=category1), "category1": category1})

def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()
            return redirect('add_recipe')
    else:
        form = RecipeForm()
    return render(request, "recipes/add_recipe.html", {"form": form})

def add_ingredient(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    return render(request, "recipes/recipe_detail.html", {})

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
    return render(request, "recipes/search.html", {"results": results, "query": q,})