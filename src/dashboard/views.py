import random
from django.views.generic import View
from django.shortcuts import render
from products.models import Product
# Create your views here.


class DashBoardView(View):

    def get(self, request, *args, **kwargs):
        # get the views for the requested user:
        # assuming that user is not logged in
        tag_views = None
        top_tags = None
        products = None
        owned = None
        try:
            # tagview_set -> tem que usar _set  pq eh foreign key
            tag_views = request.user.tagview_set.all().order_by("-count")[:5]
        except:
            pass
        try:
            # myproducts.products -> tem que usar . pq eh OneToOneField
            owned = request.user.myproducts.products.all()
        except:
            pass

        if tag_views:
            top_tags = [x.tag for x in tag_views]
            # \ :allows to add aditional things to the calls (allows to continue adding at the bottom line)
            products = Product.objects.filter(tag__in=top_tags)
            if owned:
                products = products.exclude(pk__in=owned)
            # checking if the number of clicks on a determined tag is less than some number
            # if yes, just show the user a bunch of random products (mais uma vez outra solucao porca)
            if products.count() < 10:
                products = Product.objects.all().order_by("?")
                if owned:
                    products = products.exclude(pk__in=owned)
                products = products[:10]
            else:
                products = products.distinct()
                # giving a list of randomized products. Website becomes more dynamic
                products = sorted(products, key= lambda x: random.random())

        context = {
            "products": products,
            "top_tags": top_tags,
        }

        return render(request, "dashboard/view.html", context)
