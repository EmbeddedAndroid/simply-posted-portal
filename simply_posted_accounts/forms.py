from django import forms
from django.utils.translation import ugettext_lazy as _
import account.forms

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = None


class SignupForm(account.forms.SignupForm):

    company = forms.CharField(
        label=_("Company"),
        max_length=30,
        widget=forms.TextInput(), required=True)

    first_name = forms.CharField(
        label=_("First Name"),
        max_length=30,
        widget=forms.TextInput(), required=True)

    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=30,
        widget=forms.TextInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        del self.fields["username"]
        field_order = ["company", "first_name", "last_name", "email", "password", "password_confirm", "code"]
        if not OrderedDict or hasattr(self.fields, "keyOrder"):
            self.fields.keyOrder = field_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in field_order)