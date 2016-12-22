from django.shortcuts import redirect
from django.views.generic.edit import FormView
from account.mixins import LoginRequiredMixin
from django.contrib import messages
from account.utils import default_redirect
from account.conf import settings
from account.models import EmailAddress
from django.utils.translation import ugettext_lazy as _
import account.forms
import account.views
import simply_posted_accounts.forms


class LoginView(account.views.LoginView):

    form_class = account.forms.LoginEmailForm

class SignupView(account.views.SignupView):

    form_class = simply_posted_accounts.forms.SignupForm
    identifier_field = "email"

    def after_signup(self, form):
        self.create_profile(form)
        super(SignupView, self).after_signup(form)

    def create_profile(self, form):
        self.created_user.first_name = form.cleaned_data["first_name"]
        self.created_user.last_name = form.cleaned_data["last_name"]
        self.created_user.save()
        profile = self.created_user.profile
        profile.company = form.cleaned_data["company"]
        profile.email = form.cleaned_data["email"]
        profile.save()

    def set_timezone(self,form):
        fields = {}
        fields["timezone"] = form.cleaned_data["timezone"]
        if fields:
            account = self.request.user.account
            for k, v in fields.items():
                setattr(account, k, v)
            account.save()

    def form_valid(self, form):
        super(SignupView, self).form_valid(form)
        self.set_timezone(form)
        return redirect(self.get_success_url())

    def generate_username(self, form):
        return form.cleaned_data["email"]


class VoiceView(LoginRequiredMixin, FormView):

    template_name = "account/voice.html"
    form_class = simply_posted_accounts.forms.VoiceForm
    redirect_field_name = "next"
    messages = {
        "settings_updated": {
            "level": messages.SUCCESS,
            "text": _("Voice settings updated.")
        },
    }

    def get_form_class(self):
        # @@@ django: this is a workaround to not having a dedicated method
        # to initialize self with a request in a known good state (of course
        # this only works with a FormView)
        self.primary_email_address = EmailAddress.objects.get_primary(self.request.user)
        return super(VoiceView, self).get_form_class()

    def get_initial(self):
        initial = super(VoiceView, self).get_initial()
        if self.request.user.profile.voice:
            initial["business_type"] = self.request.user.profile.voice.business_type
        return initial

    def update_voice(self, form):
        fields = {}
        if "business_type" in form.cleaned_data:
            fields["business_type"] = form.cleaned_data["business_type"]
        if fields:
            voice = self.request.user.profile.voice
            for k, v in fields.items():
                setattr(account, k, v)
            voice.save()

    def form_valid(self, form):
        self.update_voice(form)
        if self.messages.get("settings_updated"):
            messages.add_message(
                self.request,
                self.messages["settings_updated"]["level"],
                self.messages["settings_updated"]["text"]
            )
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        ctx = super(VoiceView, self).get_context_data(**kwargs)
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.POST.get(redirect_field_name, self.request.GET.get(redirect_field_name, "")),
        })
        return ctx

    def update_account(self, form):
        pass

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.VOICE_SETTINGS_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)