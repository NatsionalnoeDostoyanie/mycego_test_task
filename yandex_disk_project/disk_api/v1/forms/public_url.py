"""
A form module that works with public URLs.
"""

from django import forms
from django.utils.translation import gettext_lazy as _


class PublicUrlInputForm(forms.Form):
    """
    Form for entering public URL.

    This form is intended to obtain a public URL that will be used to interact with resources on Yandex Disk.
    It includes one required field to enter the URL.
    """

    public_url = forms.CharField(label=_("Public url"), max_length=255, required=True)
