# Testing the view functions

from django.test import TestCase
from django.urls import resolve, reverse
from recipes import views
from recipes.models import Category, Recipe
from django.contrib.auth.models import User


class RecipeViewsTest(TestCase):
    def test_home_view_function(self):
        # tests if the home view function is correct

        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_home_view_status_code(self):
        # tests if the home view status code is 200

        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        # tests if the home view template is correct

        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_home_view_is_empty(self):
        # tests if the home view function shows nothing
        # when there is no recipes

        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1> No recipes found here :( </h1>',
            response.content.decode('utf-8'))

    def test_home_view_template_recipes(self):
        # tests if the home view template loads the registered recipes

        category = Category.objects.create(name='Category_1')
        author = User.objects.create_user(
            first_name='John',
            last_name='Sikes',
            username='john_sikes',
            password='12345',
            email='johnsikes@gmail.com',
        )
        recipe = Recipe.objects.create(
            title = 'Recipe title',
            description = 'Recipe description',
            slug = 'Recipe slug',
            preparation_time = 10,
            preparation_time_unit = 'minutes',
            servings = 5,
            servings_unit = 'portions',
            preparation_steps = 'Preparation steps',
            preparation_steps_is_html = False,
            is_published = True,
            category=category,
            author=author,
        )
        ...

# --------------------------------------------------------------------------------------

    def test_category_view_function(self):
        # tests if the recipe category view function is correct

        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_category_view_is_empty(self):
        # tests if the recipe category view function returns
        # status code 404 when there is no recipes

        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1000}))  # noqa: E501
        self.assertEqual(response.status_code, 404)

# --------------------------------------------------------------------------------------

    def test_recipe_detail_view_function(self):
        # tests if the recipe details view function is correct

        view = resolve(reverse('recipes:details', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_is_empty(self):
        # tests if the recipe details view function returns
        # status code 404 when there is no recipe

        response = self.client.get(reverse('recipes:details', kwargs={'id': 100}))  # noqa: E501
        self.assertEqual(response.status_code, 404)