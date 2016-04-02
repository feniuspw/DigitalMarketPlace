import datetime
from django.db.models import Count, Min, Max, Avg, Sum
from .models import SellerAccount
from digitalmarket.mixins import LoginRequiredMixin
from products.models import Product, MyProducts
from billing.models import Transaction


# pra usar aggregation TEM que ser uma QUERYSET!!!!
# pode usar o aggregation com varios modos como Sum, Avg entre outros
# ex:  ....agregation(Sum("column), Avg("column"))
# retornaria  {"column__sum":sum,
#              "column__avg":avg,
#               }

"""
PARAMETROS PASSADOS COM * CRIAM UMA TUPLA
PARAMETROS PASSADOS COM ** CRIA UM DICIONARIO
"""

class SellerAccountMixin(LoginRequiredMixin, object):
    account = None
    products = []
    transactions = []

    def get_account(self):
        user = self.request.user
        accounts = SellerAccount.objects.filter(user=user)
        if accounts.exists() and accounts.count() == 1:
            self.account = accounts.first()
            return accounts.first()
        return None

    def get_products(self):
        account = self.get_account()
        products = Product.objects.filter(seller=account)
        self.products = products
        return products

    # Se o produto vem de outro vendedor, nao aparece em transacoes

    def get_products_fix(self):
        # TODO: VERIFICAR SE ESSA BUSCA EM MYPRODUCTS PODE RETORNAR VAZIO!!!!!!
        account = self.get_account()
        myproducts = MyProducts.objects.filter(user=account.user).first()
        products = myproducts.products.all()
        self.products = products
        return products

    def get_transactions(self):
        products = self.get_products_fix()
        transactions = Transaction.objects.filter(product__in=products)
        return transactions

    def get_transactions_today(self, transactions):
        today = datetime.date.today()
        today_min = datetime.datetime.combine(today, datetime.time.min)
        today_max = datetime.datetime.combine(today, datetime.time.max)
        print(today,today_min,today_max)
        # (igual o do tutorial) usando get_transactions_today(self):
        # return self.get_transactions().filter(timestamp__range=(today_min, today_max))
        # meu jeito
        return transactions.filter(timestamp__range=(today_min, today_max))

    def get_total_sales(self):
        t = self.get_transactions().aggregate(Sum("price"))
        total_sales = t["price__sum"]
        return total_sales

    def get_today_sales(self, transactions):
        t = self.get_transactions_today(transactions).aggregate(Sum("price"))
        total_sales = t["price__sum"]
        return total_sales
