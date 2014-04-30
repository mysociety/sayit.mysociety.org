from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from instances.models import Instance

class InstanceCreate(CreateView):
    model = Instance
    fields = [ 'label', 'title', 'description' ]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InstanceCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        redirect = super(InstanceCreate, self).form_valid(form)
        self.object.users.add(self.request.user)
        return redirect
