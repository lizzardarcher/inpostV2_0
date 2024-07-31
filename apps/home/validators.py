from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_contains_https(value):
    if 'https://t.me/' not in value:
        raise ValidationError(
            _('%(value)s | Поле должно содержать ссылку вида: https://t.me/bla-bla-bla'),
            params={'value': value},
        )


def validate_post_name(value):
    if not value:
        raise ValidationError(
            _('%(value)s | Назовите ваш пост, например пост-1 или как-нибудь ещё'),
            params={'value': value},
        )


def validate_bot_name(value):
    if 'http' not in value and '://' not in value:
        raise ValidationError(
            _('%(value)s | Введите корректную ссылку, включающую в себя http:// или https://'),
            params={'value': value},
        )


def post_ref_validator(value):
    if 'http' not in value and '://' not in value:
        raise ValidationError(
            _('%(value)s | Введите корректную ссылку, включающую в себя http:// или https://'),
            params={'value': value},
        )