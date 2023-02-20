from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def add_attr(field, attr_name, new_attr_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {new_attr_val}'.strip()

def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            ('Password length must be at least 8 characters and must '
             'contain an uppercase letter, a lowercase letter, and a number.'),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Type an username')
        add_placeholder(self.fields['email'], 'Type your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Wheeler')
        add_placeholder(self.fields['password'], 'Type a password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

    username = forms.CharField(
        label='Username',
        help_text='Length must have at least 6 characters. Letters, digits and @/./+/-/_ only.',
        error_messages={
            'required': 'This field must not be empty.',
            'min_length': 'Username must be at least 6 characters long',
            'max_length': 'Username can be up to 20 characters long.',
        },
        min_length=6,
        max_length=20
    )

    first_name = forms.CharField(
        error_messages={
            'required': 'Write your first name.'
        },
        label='First name',
    )

    last_name = forms.CharField(
        error_messages={
            'required': 'Write your last name.'
        },
        label='Last name',
    )

    email = forms.EmailField(
        error_messages={
            'required': 'E-mail is required.'
        },
        label='E-mail',
        help_text='Type a valid e-mail address.',

    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty.',
        },
        help_text=(
            'Password length must be at least 8 characters and must '
            'contain an uppercase letter, a lowercase letter, and a number.'
        ),
        validators=[strong_password],
        label='Password',

    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Please, repeat your password.',
        },
        label='Password2'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError('The e-mail is already being used', code='invalid')

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_error = ValidationError(
                'Password and password2 must be equal.',
                code='invalid'
            )

            raise ValidationError({
                'password': password_error,
                'password2': [
                    password_error,
                ],
            })
