from .test_recipe_base import RecipeTestBase
from django.urls import resolve, reverse
from recipes import views
from unittest.mock import patch

class RecipeHomeViewTest(RecipeTestBase):
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
        # tests if the home view template loads the recipes

        # first we need to create a recipe
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        context_recipes = response.context['recipes']

        # now we test if the template loads some elements
        self.assertIn('Recipe title', content)
        self.assertEqual(len(context_recipes), 1)

    def test_home_view_template_dont_show(self):
        # tests if the home view template do not load the recipes when it
        # is with is_published = False

        # first we need to create a recipe
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        # now we test if the template loads some elements
        self.assertIn(
            '<h1> No recipes found here :( </h1>',
            response.content.decode('utf-8'))

    def test_home_view_is_paginated(self):
        for i in range(0, 10):
            kwargs = {'author_data': {'username': f'u{i}'}, 'slug': f'r{i}'}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 4)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 3)
            self.assertEqual(len(paginator.get_page(4)), 1)