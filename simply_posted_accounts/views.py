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

    def after_signup(self, form):
        self.create_profile(form)
        super(SignupView, self).after_signup(form)

    def create_profile(self, form):
        profile = self.created_user.profile
        profile.company = form.cleaned_data["company"]
        profile.website = form.cleaned_data["website"]
        profile.email = form.cleaned_data["email"]
        profile.first_name = form.cleaned_data["first_name"]
        profile.last_name = form.cleaned_data["last_name"]
        profile.save()

    def generate_username(self, form):
        # do something to generate a unique username (required by the
        # Django User model, unfortunately)
        username = hashlib.sha1("Nobody inspects the spammish repetition").hexdigest()
        return username