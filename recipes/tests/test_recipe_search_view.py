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
