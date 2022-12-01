from .test_recipe_base import RecipeTestBase
from django.urls import resolve, reverse
from recipes import views

class RecipeCategoryViewTest(RecipeTestBase):
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