from .test_recipe_base import RecipeTestBase
from django.urls import resolve, reverse
from recipes import views

class RecipeSearchViewTest(RecipeTestBase):
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
    
    def test_search_by_title(self):
        # tests if the search function can find
        # a recipe by its title

        title1 = 'Title recipe one'
        title2 = 'Title recipe two'

        recipe1 = self.make_recipe(
            title=title1,
            slug='recipe-one-slug',
            author_data={
                'username': 'username1'
            }
        )
        recipe2 = self.make_recipe(
            title=title2,
            slug='recipe-two-slug',
            author_data={
                'username': 'username2'
            }
        )

        url = reverse('recipes:search')
        response1 = self.client.get(f'{url}?q={title1}')
        response2 = self.client.get(f'{url}?q={title2}')
        response_both = self.client.get(f'{url}?q=title') # the word 'title' is in both recipes

        self.assertIn(recipe1, response1.context['recipes']) # recipe1 must be in response1
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes']) # recipe2 must be in response2
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])