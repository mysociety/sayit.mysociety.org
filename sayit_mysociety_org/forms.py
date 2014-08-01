from django import forms
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class ShareForm(forms.Form):
    email = forms.EmailField(label=_('E-mail'))

    # largely cargo-culted from allauth.account.forms.ResetPasswordForm
    def clean_email(self):
        email = self.cleaned_data["email"]
        # email = get_adapter().clean_email(email)
        self.users = User.objects \
            .filter(Q(email__iexact=email)
                    | Q(emailaddress__email__iexact=email)).distinct()
        return self.cleaned_data["email"]
