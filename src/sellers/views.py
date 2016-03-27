from django.shortcuts import render
from django.views.generic import View
# Create your views here.

from digitalmarket.mixins import LoginRequiredMixin
from .forms import NewSellerForm
from .models import SellerAccount
from django.views.generic.edit import FormMixin


class SellerDashboard(LoginRequiredMixin, FormMixin, View):
    form_class = NewSellerForm
    success_url = "/seller/"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        # one way to get the form
        # apply_form = NewSellerForm()
        # since we have FormMixin we can use this way:
        apply_form = self.get_form()
        account = SellerAccount.objects.filter(user=self.request.user)
        exists = account.exists()
        context = {}
        if not exists:
            context['title'] = "Apply for an account"
            context['apply_form'] = apply_form
        else:
            account = account.first()
            active = account.active
            context['active'] = active
            context['account'] = account
            if active:
                context['title'] = "Dashboard"
            else:
                context['title'] = "Account Pending"

        return render(request, "sellers/dashboard.html", context)

    def form_valid(self, form):
        valid_data = super(SellerDashboard, self).form_valid(form)
        obj = SellerAccount.objects.create(user=self.request.user)
        return valid_data
