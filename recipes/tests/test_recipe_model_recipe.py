from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized

class RecipeTestModel(RecipeTestBase):
    # tests the model

    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_a_recipe(self):
        # make a recipe with
        recipe = Recipe(
            category=self.make_category(name='new_category'),
            author=self.make_author(username='new_user'),
            title='Recipe title',
            description='Recipe description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='minutes',
            servings=5,
            servings_unit='portions',
            preparation_steps='Preparation steps',
        )
        recipe.full_clean()
        recipe.save()

        return recipe


    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])

    def test_model_fields_max_length(self, field, max_length):
        # if the length of the given field is greater than
        # the max_length, a ValidationError will be raised

        setattr(self.recipe, field, 'A'*(max_length+1))
        with self.assertRaises(expected_exception=ValidationError):
            self.recipe.full_clean()

    def test_model_field_preparation_steps_is_html(self):
        # tests if the field preparation_steps_is_html
        # is False by default
        recipe = self.make_a_recipe()

        self.assertFalse(recipe.preparation_steps_is_html)

    def test_model_field_is_published(self):
        # tests if the field is_published
        # is False by default
        recipe = self.make_a_recipe()

        self.assertFalse(recipe.is_published)

    def test_recipe_string_representation(self):
        # tests if the string representation of a recipe
        # is the same as the recipe's title

        self.recipe.title = 'Testing representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Testing representation')