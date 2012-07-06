# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _


class ZmanForm(forms.Form):

    owed_username = forms.CharField(max_length=128, label=_('Who do you owe?'),
                                    help_text=_("This will be their twitter handle"))
    amount = forms.IntegerField(min_value=1,
                                max_value=100, label=_("How many?"))

    def clean(self):
        """removes the @ symbole if it is present"""
        cleaned_data = super(ZmanForm, self).clean()
        fixed_username = cleaned_data.get('owed_username', '').replace('@', '')
        cleaned_data['owed_username'] = fixed_username
        return cleaned_data
