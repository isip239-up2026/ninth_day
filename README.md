# Кулинарная книга — учебный проект

## Быстрый старт

```bash
pip install django
python manage.py migrate
python seed.py          # загрузить данные
python manage.py runserver
```

Открыть: http://127.0.0.1:8000  
Админка: http://127.0.0.1:8000/admin — логин `admin` / пароль `admin`

---

## Структура проекта

```
ninth_day/
├── cookbook/               # настройки проекта
│   ├── settings.py
│   └── urls.py
├── recipes/                # приложение
│   ├── models.py           # Category, Recipe, Ingredient, Favorite
│   ├── views.py            # index, recipe_detail
│   ├── urls.py
│   ├── admin.py
│   └── templates/recipes/
│       ├── base.html
│       ├── index.html
│       └── recipe_detail.html
├── seed.py
└── db.sqlite3
```

## Модели

```
Category   — name, icon
Recipe     — title, description, category(FK), author, cooking_time, servings, image_url, created_at
Ingredient — recipe(FK), name, amount
Favorite   — recipe(FK), ip_address, created_at
```

## Страницы

| URL | Описание |
|-----|----------|
| `/` | Список всех рецептов |
| `/recipe/<id>/` | Страница рецепта |

---

## Задания для студентов

> ⚠️ Задания выполняются **последовательно**. Каждый студент создаёт свою ветку,
> выполняет задание.

### Порядок работы

### Task 1 — Фильтрация по категориям
**Файлы:** `recipes/views.py`, `recipes/urls.py`, `recipes/templates/recipes/index.html`, `recipes/templates/recipes/recipe_detail.html`, `recipes/templates/recipes/category.html` (создать)

Сейчас категории у рецептов есть, но никак не используются для навигации. Нужно добавить фильтрацию.

Что сделать:
1. В view `index` добавить в контекст все категории: `categories = Category.objects.all()`
2. В `index.html` в блоке `ЗАДАНИЕ 1` вывести кнопки-фильтры по категориям — Bootstrap `btn-outline-success` для каждой категории с иконкой и названием
3. Добавить маршрут `/category/<int:category_id>/` в `urls.py` и view `category_recipes`
4. View `category_recipes` фильтрует рецепты: `Recipe.objects.filter(category=category)`
5. Создать `category.html` — список рецептов категории, заголовок с иконкой и названием, счётчик: «10 рецептов»
6. В `recipe_detail.html` в хлебных крошках в блоке `ЗАДАНИЕ 1` добавить ссылку на страницу категории

---

### Task 2 — Форма добавления рецепта
**Файлы:** `recipes/forms.py` (создать), `recipes/views.py`, `recipes/urls.py`, `recipes/templates/recipes/add_recipe.html` (создать), `recipes/templates/recipes/base.html`

Task 1 уже добавил категории — теперь форма должна давать выбрать категорию из существующих.

Что сделать:
1. Создать `recipes/forms.py` с классом `RecipeForm` на основе `ModelForm`:
```python
from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description", "category",
                  "author", "cooking_time", "servings", "image_url"]
```
2. Добавить Bootstrap-виджеты всем полям через `widgets` в `Meta` — класс `form-control` для текстовых полей, `form-select` для `category`
3. Добавить маршрут `/add/` и view `add_recipe`
4. View обрабатывает GET (показывает форму) и POST (сохраняет рецепт, редиректит на его страницу)
5. Создать `add_recipe.html` с Bootstrap-формой и кнопкой «Сохранить рецепт»
6. В `base.html` в блоке `ЗАДАНИЕ 2` добавить ссылку «Добавить рецепт» в навбар

---

### Task 3 — Список ингредиентов и форма добавления
**Файлы:** `recipes/forms.py`, `recipes/views.py`, `recipes/urls.py`, `recipes/templates/recipes/recipe_detail.html`

Ингредиенты уже есть в БД и в модели, но на странице рецепта показывается заглушка. Task 2 уже создал `forms.py` — нужно добавить туда новую форму.

Что сделать:
1. В `forms.py` добавить класс `IngredientForm`:
```python
from .models import Ingredient

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "amount"]
```
2. В view `recipe_detail` добавить в контекст `ingredients = recipe.ingredients.all()` и пустой `IngredientForm()`
3. В `recipe_detail.html` в блоке `ЗАДАНИЕ 3` вывести ингредиенты таблицей Bootstrap — колонки «Ингредиент» и «Количество», чередующиеся строки через `table-striped`
4. Добавить маршрут `/recipe/<int:recipe_id>/add-ingredient/` и view `add_ingredient`
5. View обрабатывает POST: сохраняет ингредиент, привязывает к рецепту, редиректит обратно
6. В шаблоне показать форму добавления ингредиента под таблицей

---

### Task 4 — Поиск и сортировка
**Файлы:** `recipes/views.py`, `recipes/urls.py`, `recipes/templates/recipes/base.html`, `recipes/templates/recipes/index.html`, `recipes/templates/recipes/search.html` (создать)

Task 1 уже добавил категории, Task 2 — форму добавления. Поиск должен охватывать и новые рецепты.

Что сделать:
1. В `base.html` в блоке `ЗАДАНИЕ 4` добавить GET-форму поиска в навбар
2. Добавить маршрут `/search/` и view `search`
3. Искать одновременно по названию, автору и категории:
```python
from django.db.models import Q
results = Recipe.objects.filter(
    Q(title__icontains=q) |
    Q(author__icontains=q) |
    Q(category__name__icontains=q)
)
```
4. Создать `search.html` — карточки результатов или «Ничего не найдено по запросу "..."»
5. В `index.html` в блоке `ЗАДАНИЕ 4` добавить кнопки сортировки: «По времени» (`cooking_time`), «По дате» (`-created_at`), «По алфавиту» (`title`)
6. В view `index` применять сортировку через `request.GET.get('sort', '-created_at')`

---

### Task 5 — Избранное
**Файлы:** `recipes/views.py`, `recipes/urls.py`, `recipes/templates/recipes/recipe_detail.html`, `recipes/templates/recipes/index.html`, `recipes/templates/recipes/favorites.html` (создать), `recipes/templates/recipes/base.html`

Финальное задание — использует всё что сделали предыдущие: категории, рецепты, ингредиенты. Модель `Favorite` уже есть.

Что сделать:
1. Добавить маршруты `/recipe/<id>/favorite/` и `/favorites/`
2. View `toggle_favorite`: получить IP через `request.META.get('REMOTE_ADDR')`, если запись есть — удалить, нет — создать. Редирект обратно на рецепт
3. В `recipe_detail.html` в блоке `ЗАДАНИЕ 5` добавить кнопку «❤️ В избранное» или «💔 Убрать» в зависимости от наличия в списке. В блоке счётчика показать реальное число
4. В `index.html` в блоке `ЗАДАНИЕ 5` добавить в футер карточки счётчик: «❤️ 3»
5. Создать `favorites.html` — все рецепты текущего IP в избранном, карточками как на главной
6. В `base.html` в блоке `ЗАДАНИЕ 5` добавить ссылку «❤️ Избранное» в навбар
