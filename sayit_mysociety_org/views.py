import hashlib
import urlparse

from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.http import int_to_base36
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages

from allauth.account.adapter import get_adapter
from allauth.account.views import PasswordResetFromKeyView

from instances.models import Instance
from instances.views import InstanceFormMixin

from forms import ShareForm


class InstanceCreate(CreateView):
    model = Instance
    fields = ['label', 'title', 'description']

    def is_stashed(self):
        return self.request.GET.get('post') and self.request.session.get('instance')

    def get(self, request, *args, **kwargs):
        if self.is_stashed():
            return self.post(request, *args, **kwargs)
        return super(InstanceCreate, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(InstanceCreate, self).get_form_kwargs()
        if self.is_stashed():
            kwargs['data'] = self.request.session['instance']
            del self.request.session['instance']
        return kwargs

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            form.instance.created_by = self.request.user
            redirect = super(InstanceCreate, self).form_valid(form)
            self.object.users.add(self.request.user)
            return redirect
        else:
            self.request.session['instance'] = form.cleaned_data
            return redirect_to_login(
                self.request.path + '?post=1',
                login_url=reverse("account_signup"),
            )


class ShareWithCollaborators(FormView, InstanceFormMixin):
    template_name = 'share_instance_with_collaborators.html'

    form_class = ShareForm
    success_url = reverse_lazy('share_instance')

    # substantially cargo-culted from allauth.account.forms.ResetPasswordForm
    def form_valid(self, form):
        email = form.cleaned_data["email"]

        users = form.users
        if users:
            context = {"instance": self.request.instance}
            get_adapter().send_mail('instance_invite_existing',
                                    email,
                                    context)
            user_ids = [x.id for x in users]

        else:
            # Create a new user with email address as username
            # or a bit of a hash of the email address if it's longer
            # than Django's 30 character username limit.
            if len(email) > 30:
                username = hashlib.md5(email).hexdigest()[:10]
            else:
                username = email

            # Let's try creating a new user and sending an email to them
            # with a link to the password reset page.
            # FIXME - should probably try/catch the very unlikely situation
            # where we have a duplicate username, I guess.
            user = User.objects.create_user(username, email=email)
            user_ids = (user.id,)

            temp_key = default_token_generator.make_token(user)

            instance_url = self.request.instance.get_absolute_url()

            # send the password reset email
            path = reverse("instance_accept_invite",
                           kwargs=dict(uidb36=int_to_base36(user.id),
                                       key=temp_key))
            url = urlparse.urljoin(instance_url, path)
            context = {
                "instance": self.request.instance,
                "user": user,
                "password_reset_url": url,
                }
            get_adapter().send_mail('accept_invite',
                                    email,
                                    context)

        self.request.instance.users.add(*user_ids)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Your invitation has been sent. Would you like to send another?',
            )
        return super(ShareWithCollaborators, self).form_valid(form)


class AcceptInvite(PasswordResetFromKeyView):
    template_name = 'accept_invitation.html'

    def get_success_url(self):
        return reverse('speeches:home')


from allauth.account.signals import password_reset
from django.dispatch import receiver

@receiver(password_reset, dispatch_uid="invite_accepted")
def login_on_invite_accepted_callback(sender, **kwargs):
    request = kwargs['request']

    # It's very ugly to be using the path here, but I can't
    # see any other easy way to make this signal handler work
    # only for invite related password resets
    if request.path_info.startswith('/instance/invite/'):
        user = kwargs['user']
        get_adapter().login(request, user)
