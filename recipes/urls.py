from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipe/<int:recipe_id>/", views.recipe_detail, name="recipe_detail"),
    path("category/<int:category_id>/", views.category_recipes, name="category_recipes"),
    path("add/", views.add_recipe, name="add_recipe"),
    path("recipe/<int:recipe_id>/add-ingredient/", views.add_ingredient, name="add_ingredient"),
    path("search/", views.search, name="search")
]
