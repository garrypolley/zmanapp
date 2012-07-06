# -*- coding: utf-8 -*-

from .models import OwedItem
from django import forms
from django.utils.translation import ugettext_lazy as _


class ZmanForm(forms.Form):

    owed_username = forms.CharField(max_length=128, label=_('Who do you owe?'),
                                    help_text=_("This will be their twitter handle"))
    amount = forms.IntegerField(min_value=1,
                                max_value=100, label=_("How many?"))
