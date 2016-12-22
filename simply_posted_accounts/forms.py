from django import forms
from django.utils.translation import ugettext_lazy as _
from account.conf import settings
import account.forms

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = None


class SignupForm(account.forms.SignupForm):

    first_name = forms.CharField(
        label=_("First Name"),
        max_length=30,
        widget=forms.TextInput(), required=True)

    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=30,
        widget=forms.TextInput(), required=True)

    timezone = forms.ChoiceField(
        label=_("Timezone"),
        choices=[("", "---------")] + settings.ACCOUNT_TIMEZONES,
        required=True)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        del self.fields["username"]
        field_order = ["first_name", "last_name", "email", "password",
                       "password_confirm", "timezone", "code"]
        if not OrderedDict or hasattr(self.fields, "keyOrder"):
            self.fields.keyOrder = field_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in field_order)