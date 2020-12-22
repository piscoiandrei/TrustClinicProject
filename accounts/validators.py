from django.core.exceptions import ValidationError


def personal_id_validator(value):
    for c in value:
        if c not in "0123456789":
            raise ValidationError('The personal ID must only contain digits.')


def phone_validator(value):
    if len(value) >= 16:
        raise ValidationError('Incorrect phone number format.')

    if '+' in value and value[0] != '+':
        raise ValidationError('Incorrect phone number format.')

    for c in value:
        if c not in '0123456789+ -()':
            raise ValidationError(
                'The phone number contains forbbiden characters')
