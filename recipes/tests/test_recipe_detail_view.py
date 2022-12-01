from .test_recipe_base import RecipeTestBase
from django.urls import resolve, reverse
from recipes import views

class RecipeDetailViewTest(RecipeTestBase):
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