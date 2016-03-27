from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from .decorators import ajax_required


class AjaxRequiredMixin(object):
    # method that is called when it's going to send data back
    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxRequiredMixin, self).dispatch(request, *args, **kwargs)


class LoginRequiredMixin(object):
    # method that is called when it's going to send data back
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class StaffRequiredMixin(object):
    # method thar is called when it's going to send data back
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


class MultiSlugMixin(object):
    model = None

    def get_object(self,  *args, **kwargs):
        slug = self.kwargs.get("slug")
        model_class = self.model
        if slug is not None:
            try:
                obj = get_object_or_404(model_class, slug=slug)
            except model_class.MultipleObjectsReturned:
                obj = obj.filter(slug=slug).order_by("-title").first()
        else:
            obj = super(MultiSlugMixin, self).get_object(*args, **kwargs)
        return obj


class SubmitBtnMixin(object):
    submit_btn = None

    def get_context_data(self, *args, **kwargs):
        context = super(SubmitBtnMixin, self).get_context_data(*args, **kwargs)
        context["submit_btn"] = self.submit_btn
        return context
