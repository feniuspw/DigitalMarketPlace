from django.shortcuts import render
from django.views.generic import View

# Create your views here.

from digitalmarket.mixins import LoginRequiredMixin
from .mixins import SellerAccountMixin
from .forms import NewSellerForm
from .models import SellerAccount
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404

from billing.models import Transaction
from products.models import Product


class SellerProductDetailRedirectView(RedirectView):

    permanent = True
    # query_string = True
    # pattern_name = 'article-detail'

    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Product, pk=kwargs['pk'])
        return obj.get_absolute_url()


class SellerTransactionListView(SellerAccountMixin, ListView):
    model = Transaction
    template_name = 'sellers/transaction_list_view.html'

    def get_queryset(self):
        return self.get_transactions()
        # account = SellerAccount.objects.filter(user=self.request.user)
        # if account.exists():
        #     products = Product.objects.filter(seller=account)
        #     return Transaction.objects.filter(product__in=products)
        # return []


class SellerDashboard(SellerAccountMixin, FormMixin, View):
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
        # with mixin
        account = self.get_account()
        # without mixin
        # account = SellerAccount.objects.filter(user=self.request.user)
        # exists = account.exists()
        context = {}
        if not account:
            context['title'] = "Apply for an account"
            context['apply_form'] = apply_form
        else:
            # without mixin
            # account = account.first()
            active = account.active
            context['active'] = active
            context['account'] = account
            if active:
                context['title'] = "Dashboard"


                # with mixin
                context['products'] = self.get_products()

                transactions = self.get_transactions()
                transactions_today = self.get_transactions_today(transactions)

                context['transactions_today'] = transactions_today
                context['today_sales'] = self.get_today_sales(transactions)
                context['total_sales'] = self.get_total_sales()
                context['transactions'] = transactions.exclude(pk__in=transactions_today)[:10]

                # without mixin
                # products = Product.objects.filter(seller=account)
                # context['products'] = products
                # context['transactions'] = Transaction.objects.filter(product__in=products)[:10]
            else:
                context['title'] = "Account Pending"

        return render(request, "sellers/dashboard.html", context)

    def form_valid(self, form):
        valid_data = super(SellerDashboard, self).form_valid(form)
        obj = SellerAccount.objects.create(user=self.request.user)
        return valid_data
