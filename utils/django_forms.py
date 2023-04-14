import re
from django.core.exceptions import ValidationError

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