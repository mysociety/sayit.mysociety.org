from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login

from instances.models import Instance

class InstanceCreate(CreateView):
    model = Instance
    fields = [ 'label', 'title', 'description' ]

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
            return redirect_to_login(self.request.path + '?post=1')
