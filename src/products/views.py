from django.shortcuts import render
# Create your views here.
from .models import Product


# one item
def detail_view(request):
    # html template
    if request.user.is_authenticated():
        template = "products/detail_view.html"
        product = Product.objects.all().first()
        # dictionary of values
        context = {
                   'object': product
                   }
    else:
        template = "products/not_found.html"
        context = {}
    return render(request, template, context)


# list of items
def list_view(request):

    # html template
    template = "products/list_view.html"

    queryset = Product.objects.all()

    # dictionary of values
    context={'queryset':queryset}
    return render(request, template, context)