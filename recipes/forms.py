from django import forms
from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title", "description", "category",
            "author", "cooking_time", "servings", "image_url",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "author": forms.TextInput(attrs={"class": "form-control"}),
            "cooking_time": forms.NumberInput(attrs={"class": "form-control"}),
            "servings": forms.NumberInput(attrs={"class": "form-control"}),
            "image_url": forms.URLInput(attrs={"class": "form-control"}),
        }


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "amount"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например: Лук"}),
            "amount": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например: 2 шт."}),
        }