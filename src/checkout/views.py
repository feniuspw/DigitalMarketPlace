import datetime
from django.http import HttpResponse, JsonResponse
from django.http import Http404 # just to see what it looks like when an error comes
from django.views.generic import View
from django.shortcuts import render

# Model Imports
from products.models import Product, MyProducts
from billing.models import Transaction
# Mixin Imports
from digitalmarket.mixins import AjaxRequiredMixin
# Create your views here.


class CheckoutAjaxView(AjaxRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({}, status=401)
        # maybe credit card required here!

        # ********************************
        user = request.user
        product_id = request.POST.get("product_id")
        # se usar Product.objects.filter retorna um array que eh uma QuerySet de objetos encontrados
        # se usar Product.objects.get tenta pegar o objeto mesmo (como eh chave primaria, nao tem problema)
        # se o get der pau, ja manda envia erro. Melhor usar o filter e no final usar [0]
        #  (ou .first()) pra pegar o primeiro produto.. o unico no caso
        product_obj = Product.objects.filter(id=product_id).first()
        if not product_obj:
            return JsonResponse({}, status=404)

        # run transaction
        # assume it's successful
        trans_obj = Transaction.objects.create(user=request.user,
                                               product=product_obj,
                                               price=product_obj.get_price,
                                               )

        my_products = MyProducts.objects.get_or_create(user=request.user)[0]
        my_products.products.add(product_obj)

        download_link = product_obj.get_download()
        preview_link = download_link + "?preview=True"

        data = {
            "download": download_link,
            "preview": preview_link,
        }
        return JsonResponse(data)


class CheckoutTestView(View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            # raise Http404
            data = {
                "works": True,
                "time": datetime.datetime.now(),
            }
            return JsonResponse(data)
        return HttpResponse('hello there')

    def get(self, request, *args, **kwargs):
        template = "checkout/test.html"
        context = {}
        return render(request,template,context)
