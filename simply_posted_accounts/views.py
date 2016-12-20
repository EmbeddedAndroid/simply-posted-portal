from django.shortcuts import render
import account.forms
import account.views
import simply_posted_accounts.forms
import hashlib


class LoginView(account.views.LoginView):

    form_class = account.forms.LoginEmailForm

class SignupView(account.views.SignupView):

    form_class = simply_posted_accounts.forms.SignupForm
    identifier_field = "email"

    def generate_username(self, form):
        # do something to generate a unique username (required by the
        # Django User model, unfortunately)
        username = hashlib.sha1("Nobody inspects the spammish repetition").hexdigest()
        return username