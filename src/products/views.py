from django.shortcuts import render
# Create your views here.
from .forms import ProductAddForm, ProductModelForm
from .models import Product

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect


def create_view(request):
    #Easy way to create forms
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        # form.save()
        # this code below does not save the form yet, but creates an instance of the object
        # if you want to change something before saving
        instance = form.save(commit=False)
        instance.sale_price = instance.price
        instance.save()

    # Hard way to create forms
    # form = ProductAddForm(request.POST or None)
    # if form.is_valid():
    #     data = form.cleaned_data
    #     title = data.get("title")
    #     description = data.get("description")
    #     price = data.get("price")
    #     # one way
    #     # new_obj = Product.objects.create(title=title, description=description, price=price)
    #     # another way
    #     # new_obj = Product()
    #     # new_obj.title = title
    #     # new_obj.description = description
    #     # new_obj.price = price
    #     # new_obj.save()
    #     # third way
    #     new_obj = Product(title=title, description=description, price = price)
    #     new_obj.save()
    template = "products/create_view.html"
    context = {
       "form": form
    }
    return render(request, template, context)


# one item
def detail_slug_view(request, slug=None):
    try:
        product = get_object_or_404(Product, slug=slug)
    except Product.MultipleObjectsReturned:
        product = Product.objects.filter(slug=slug).order_by("-title").first()

    template = "products/detail_view.html"
    context = {'object': product}
    return render(request, template, context)


# one item
def detail_view(request, object_id=None):
    product = get_object_or_404(Product, pk=object_id)
    template = "products/detail_view.html"
    context = {'object': product}
    return render(request, template, context)


# list of items
def list_view(request):

    # html template
    template = "products/list_view.html"

    queryset = Product.objects.all()

    # dictionary of values
    context={'queryset':queryset}
    return render(request, template, context)