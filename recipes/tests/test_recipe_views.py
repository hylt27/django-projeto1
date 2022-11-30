# Testing the view functions

from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase): 

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
# --------------------------------------------------------------------------------------

    def test_category_view_function(self):
        # tests if the recipe category view function is correct

        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_category_view_is_empty(self):
        # tests if the recipe category view function returns
        # status code 404 when there is no recipes

        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={
                    'category_id': 1000
                }
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_category_view_template_recipes(self):
        # tests if the category view template loads the recipes

        # first we need to create a recipe
        self.make_recipe(title='This is a test')

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        # now we test if the template loads some elements
        self.assertIn('This is a test', content)

    def test_category_view_template_dont_show(self):
        # tests if the category view template do not load the recipes when it
        # is with is_published = False

        # first we need to create a recipe
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={
                    'category_id': recipe.category.id
                }
            )
        )

        # now we test if the template loads some elements
        self.assertEqual(response.status_code, 404)
# --------------------------------------------------------------------------------------

    def test_recipe_detail_view_function(self):
        # tests if the recipe details view function is correct

        view = resolve(reverse('recipes:details', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_is_empty(self):
        # tests if the recipe details view function returns
        # status code 404 when there is no recipe

        response = self.client.get(
            reverse(
                'recipes:details',
                kwargs={
                    'id': 100
                }
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_template(self):
        # tests if the recipe detail view template loads the correct recipe

        # first we need to create a recipe
        self.make_recipe(title='Detail page of one recipe')

        response = self.client.get(
            reverse(
                'recipes:details',
                kwargs={
                    'id': 1
                }
            )
        )
        content = response.content.decode('utf-8')

        # now we test if the template loads some elements
        self.assertIn('Detail page of one recipe', content)

    def test_detail_view_template_dont_show(self):
        # tests if the recipe detail view template do not load the recipe when
        # it is with is_published = False

        # first we need to create a recipe
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:details',
                kwargs={
                    'id': recipe.id
                }
            )
        )

        # now we test if the template loads some elements
        self.assertEqual(response.status_code, 404)
# --------------------------------------------------------------------------------------

    def test_search_view_function(self):
        # tests if the search input uses
        # the correct view function

        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)
    
    def test_search_view_template(self):
        # tests if the search input loads
        # the correct template

        response = self.client.get(reverse('recipes:search') + '?q=test')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_search_view_404_error(self):
        # tests if the search input raises
        # a 404 error if there is no search term

        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_search_term(self):
        # tests if the search_term is on the page title
        # and if it is escaped

        url = reverse('recipes:search') + '?q=test'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;test&quot;',
            response.content.decode('utf-8')
        )