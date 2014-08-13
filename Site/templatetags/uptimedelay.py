from django import forms
from django.template import Context
from django.template.loader import get_template
from django import template

register = template.Library()

@register.filter
def badge_updown(is_up):
    """ Up/Down badge """

    if is_up:
        return '<span class="badge-up">UP</span>'
    elif is_up == False:
        return '<span class="badge-down">DOWN</span>'
    else:
        return '<span class="badge-unknown">?</span>'

