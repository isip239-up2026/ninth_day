from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<int:category_id>/", views.category_recipes, name="category_recipes"),
    path("recipe/<int:recipe_id>/", views.recipe_detail, name="recipe_detail"),
]