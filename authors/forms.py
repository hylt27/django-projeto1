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
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Wheeler')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty.',
        },
        help_text=(
            'Password length must be at least 8 characters and must '
            'contain an uppercase letter, a lowercase letter, and a number.'
        ),
        validators=[strong_password],
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        })
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
        # exclude = ['last_name','first_name']

        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
            'password': 'Password',
        }

        help_texts = {
            'email': 'Type a valid e-mail address.'
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty.',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name',
                'class': 'input text-input other-class'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Type your last name',
                'class': 'input text-input other-class'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password',
            })
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'attention' in data:
            raise ValidationError(
                'Do not write %(value)s in the password field.',
                code='invalid',
                params={'value': '"attention"'}
            )

        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'Henrique' in data:
            raise ValidationError(
                'Do not write %(value)s in the first name field.',
                code='invalid',
                params={'value': '"Henrique"'}
            )

        return data

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
