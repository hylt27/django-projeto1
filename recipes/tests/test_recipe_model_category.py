from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError

class CategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(name='Category test')
        return super().setUp()

    def test_category_model_string_representation(self):
        self.assertEqual(str(self.category),self.category.name)

    def test_category_model_name(self):
        # if the length of the given name is greater than
        # the max_length, a ValidationError will be raised

        self.category.name = 'A'*66

        with self.assertRaises(expected_exception=ValidationError):
            self.category.full_clean()