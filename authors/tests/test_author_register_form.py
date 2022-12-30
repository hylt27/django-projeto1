form django.test import TestCase
from authors.forms import RegisterForm

class AuthorRegisterFormUnitTest(TestCase):
    def test_first_name_placeholder(self):
        # tests if the placeholder of first_name is correct
        form = RegisterForm()
        placeholder = form['first_name'].field.widget.attrs['placeholder']
        self.assertEqual('Ex.: John', placeholder)
        

