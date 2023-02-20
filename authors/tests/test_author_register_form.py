from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Type an username'),
        ('email', 'Type your e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Wheeler'),
        ('password', 'Type a password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        # tests if the placeholder of the fields is correct
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('username', 'Length must have at least 6 characters. Letters, digits and @/./+/-/_ only.'),
        ('email', 'Type a valid e-mail address.'),
        ('password', 'Password length must be at least 8 characters and must '
            'contain an uppercase letter, a lowercase letter, and a number.'),
    ])
    def test_fields_help_text(self, field, help_text):
        # tests if the help_text of the fields is correct
        form = RegisterForm()
        current_help_text = form[field].field.help_text
        self.assertEqual(help_text, current_help_text)

    @parameterized.expand([
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label(self, field, label):
        # tests if the labels of the fields is correct
        form = RegisterForm()
        current_label = form[field].field.label
        self.assertEqual(label, current_label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1'
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty.'),
        ('first_name', 'Write your first name.'),
        ('last_name', 'Write your last name.'),
        ('password', 'Password must not be empty.'),
        ('password2', 'Please, repeat your password.'),
        ('email', 'E-mail is required.'),

    ])
    def test_fields_cant_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8')) # here we get the content rendered on screen
        self.assertIn(msg, response.context['form'].errors.get(field)) # here we get the form of the context

    def test_username_min_length(self):
        self.form_data['username'] = 'kev'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must be at least 6 characters long'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_max_length(self):
        self.form_data['username'] = 'Abcd'*20
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username can be up to 20 characters long.'
        #self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_strength(self):
        self.form_data['password'] = 'Abcd123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = (
            'Password length must be at least 8 characters and must '
            'contain an uppercase letter, a lowercase letter, and a number.'
        )
        #self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password2(self):
        # tests if the two passwords are not equal
        self.form_data['password'] = '@Abcd123ef'
        self.form_data['password2'] = '@Abcd123ef7'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Password and password2 must be equal.'
        self.assertIn(msg, response.context['form'].errors.get('password'))

        # tests if the two passwords are equal:
        self.form_data['password'] = '@Abcd123ef'
        self.form_data['password2'] = '@Abcd123ef'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_create_author_view_return_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_existing_email(self):
        # tests if the email already exists in the database
        url = reverse('authors:create')

        response1 = self.client.post(url, data=self.form_data, follow=True)
        response2 = self.client.post(url, data=self.form_data, follow=True)

        msg = 'The e-mail is already being used'
        self.assertIn(msg, response2.context['form'].errors.get('email'))
        #self.assertIn(msg, response.content.decode('utf-8'))