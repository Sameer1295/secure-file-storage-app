from django import template
from django.contrib import admin

register = template.Library()


class CustomRequest:
    def __init__(self, user):
        self.user = user


@register.simple_tag(takes_context=True)
def get_app_list(context, **kwargs):
    custom_request = CustomRequest(context['request'].user)
    app_list = admin.site.get_app_list(custom_request)
    return app_list


@register.filter(name='replace_icon')
def replace_icon(value):

    default_icon = "mdi mdi-view-dashboard"

    icon_list = {
        "groups": "mdi mdi-view-dashboard",
        "users": "mdi mdi-account",
        "questions": "mdi mdi-comment-question-outline",
    }

    icon_name = value.lower()

    if icon_name in icon_list:
        return icon_list[icon_name]
    else:
        return default_icon


@register.filter(name='is_not_master_table')
def is_not_master_table(value):
    master_tables = ['Groups', 'Users', 'Expense labels', 'Expense ranges']

    if value in master_tables:
        display = 'none'
    else:
        display = 'initial'

    return display
