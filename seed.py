import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookbook.settings")
django.setup()

from django.contrib.auth.models import User
from recipes.models import Category, Recipe, Ingredient, Favorite

Category.objects.all().delete()
Recipe.objects.all().delete()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin")
    print("Создан администратор: логин=admin пароль=admin")

cats = {n: Category.objects.create(name=n, icon=i) for n, i in [
    ("Супы",      "🍲"),
    ("Салаты",    "🥗"),
    ("Выпечка",   "🥐"),
    ("Горячее",   "🍖"),
    ("Десерты",   "🍰"),
    ("Напитки",   "🥤"),
]}

recipes_data = [
    {
        "title": "Борщ классический", "author": "Бабушка Мария",
        "category": "Супы", "cooking_time": 90, "servings": 6,
        "image_url": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=600",
        "description": "Наваристый украинский борщ со свёклой, капустой и мясом. Подаётся со сметаной и чесночными пампушками.",
        "ingredients": [("Говядина", "500 г"), ("Свёкла", "2 шт"), ("Капуста", "300 г"),
                        ("Картофель", "3 шт"), ("Морковь", "1 шт"), ("Томатная паста", "2 ст.л."),
                        ("Сметана", "для подачи")],
    },
    {
        "title": "Куриный суп с лапшой", "author": "Айгуль Сейткали",
        "category": "Супы", "cooking_time": 50, "servings": 4,
        "image_url": "https://images.unsplash.com/photo-1603105037880-880cd4edfb0d?w=600",
        "description": "Лёгкий и питательный куриный суп с домашней лапшой и свежей зеленью.",
        "ingredients": [("Курица", "600 г"), ("Лапша", "150 г"), ("Морковь", "1 шт"),
                        ("Лук", "1 шт"), ("Зелень", "пучок"), ("Соль", "по вкусу")],
    },
    {
        "title": "Греческий салат", "author": "Нурлан Бекова",
        "category": "Салаты", "cooking_time": 15, "servings": 4,
        "image_url": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=600",
        "description": "Классический греческий салат с огурцами, томатами, оливками и сыром фета.",
        "ingredients": [("Томаты", "3 шт"), ("Огурцы", "2 шт"), ("Фета", "200 г"),
                        ("Оливки", "100 г"), ("Красный лук", "0.5 шт"), ("Оливковое масло", "3 ст.л.")],
    },
    {
        "title": "Оливье", "author": "Дана Рысбекова",
        "category": "Салаты", "cooking_time": 40, "servings": 8,
        "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600",
        "description": "Традиционный новогодний салат с докторской колбасой, картофелем и майонезом.",
        "ingredients": [("Картофель", "4 шт"), ("Морковь", "2 шт"), ("Яйца", "4 шт"),
                        ("Колбаса", "300 г"), ("Огурцы солёные", "3 шт"), ("Майонез", "200 г")],
    },
    {
        "title": "Домашний хлеб", "author": "Мадина Жаксыбекова",
        "category": "Выпечка", "cooking_time": 120, "servings": 10,
        "image_url": "https://images.unsplash.com/photo-1549931319-a545dcf3bc7b?w=600",
        "description": "Мягкий домашний хлеб на дрожжах. Золотистая корочка и пористый мякиш.",
        "ingredients": [("Мука", "500 г"), ("Вода тёплая", "300 мл"), ("Дрожжи", "7 г"),
                        ("Соль", "1 ч.л."), ("Сахар", "1 ч.л."), ("Масло растительное", "2 ст.л.")],
    },
    {
        "title": "Пирог с яблоками", "author": "Айгерим Нурова",
        "category": "Выпечка", "cooking_time": 60, "servings": 8,
        "image_url": "https://images.unsplash.com/photo-1568571780765-9276ac8b75a2?w=600",
        "description": "Нежный яблочный пирог с корицей. Простой рецепт к чаепитию.",
        "ingredients": [("Яблоки", "4 шт"), ("Мука", "250 г"), ("Яйца", "3 шт"),
                        ("Сахар", "150 г"), ("Масло сливочное", "100 г"), ("Корица", "1 ч.л.")],
    },
    {
        "title": "Плов по-узбекски", "author": "Санжар Алиев",
        "category": "Горячее", "cooking_time": 100, "servings": 6,
        "image_url": "https://images.unsplash.com/photo-1596560548464-f010549b84d7?w=600",
        "description": "Настоящий узбекский плов с бараниной, морковью и специями в казане.",
        "ingredients": [("Баранина", "700 г"), ("Рис", "500 г"), ("Морковь", "400 г"),
                        ("Лук", "2 шт"), ("Чеснок", "1 головка"), ("Зира", "1 ч.л."),
                        ("Масло растительное", "150 мл")],
    },
    {
        "title": "Паста карбонара", "author": "Руслан Сейтов",
        "category": "Горячее", "cooking_time": 25, "servings": 2,
        "image_url": "https://images.unsplash.com/photo-1612874742237-6526221588e3?w=600",
        "description": "Классическая итальянская паста карбонара со сливочным соусом и беконом.",
        "ingredients": [("Спагетти", "200 г"), ("Бекон", "150 г"), ("Яйца", "3 шт"),
                        ("Пармезан", "70 г"), ("Чёрный перец", "по вкусу"), ("Соль", "по вкусу")],
    },
    {
        "title": "Шоколадный торт", "author": "Жанна Абенова",
        "category": "Десерты", "cooking_time": 90, "servings": 10,
        "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=600",
        "description": "Влажный шоколадный торт с нежным ганашем. Идеален для праздника.",
        "ingredients": [("Мука", "200 г"), ("Какао", "60 г"), ("Сахар", "250 г"),
                        ("Яйца", "3 шт"), ("Молоко", "200 мл"), ("Масло", "100 г"),
                        ("Шоколад", "200 г для ганаша")],
    },
    {
        "title": "Смузи из банана и клубники", "author": "Камила Досова",
        "category": "Напитки", "cooking_time": 5, "servings": 2,
        "image_url": "https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=600",
        "description": "Быстрый и полезный смузи из свежей клубники и банана на йогурте.",
        "ingredients": [("Банан", "1 шт"), ("Клубника", "150 г"),
                        ("Йогурт натуральный", "200 мл"), ("Мёд", "1 ч.л.")],
    },
]

for r in recipes_data:
    recipe = Recipe.objects.create(
        title=r["title"], author=r["author"],
        category=cats[r["category"]],
        cooking_time=r["cooking_time"], servings=r["servings"],
        image_url=r["image_url"], description=r["description"]
    )
    for name, amount in r["ingredients"]:
        Ingredient.objects.create(recipe=recipe, name=name, amount=amount)

print(f"Готово: {Category.objects.count()} категорий, "
      f"{Recipe.objects.count()} рецептов, "
      f"{Ingredient.objects.count()} ингредиентов.")
