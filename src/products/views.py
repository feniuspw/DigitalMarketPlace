from django.shortcuts import render
# Create your views here.
from .forms import ProductAddForm, ProductModelForm
from .models import Product

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

# ------------------------ CLASS BASED VIEWS ------------------------
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
# -------------------------------------------------------------------
from digitalmarket.mixins import MultiSlugMixin, SubmitBtnMixin, LoginRequiredMixin
from .mixins import ProductManagerMixin

from django.core.urlresolvers import reverse




# ************************************* CLASS BASED VIEWS ********************************************


class ProductCreateView(LoginRequiredMixin, SubmitBtnMixin, CreateView):
    model = Product
    form_class = ProductModelForm
    template_name = "products/form.html"
    #success_url = "/product/list"
    submit_btn = "Add Product"

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        valid_data = super(ProductCreateView, self).form_valid(form)
        form.instance.managers.add(user)
        # todo: add all default users
        return valid_data

    # just showing that I can use reverse in this function as well
    # def get_success_url(self):
    #     return reverse("products:list")




class ProductDetailView(MultiSlugMixin, DetailView):
    model = Product


class ProductListView(ListView):
    model = Product
    # template_name = "products/list_view.html"
    #
    # def get_context_data(self, **kwargs):
    #     context = super(ProductListView, self).get_context_data(**kwargs)
    #     context["queryset"] = self.get_queryset()
    #     return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(**kwargs)
        return qs


class ProductUpdateView(ProductManagerMixin, SubmitBtnMixin, MultiSlugMixin, UpdateView):
    model = Product
    form_class = ProductModelForm
    template_name = "products/form.html"
    success_url = "/product/list"
    submit_btn = "Update Product"

    # def get_object(self, *args, **kwargs):
    #     user = self.request.user
    #     obj = super(ProductUpdateView, self).get_object(*args, **kwargs)
    #     if obj.user == user or user in obj.managers.all():
    #         return obj
    #     else:
    #         raise Http404




# ****************************************************************************************************

# *********************************** FUNCTION BASED VIEWS *******************************************
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
    template = "products/form.html"
    context = {
        "form": form,
        "submit_btn": "Create Product",
    }
    return render(request, template, context)


def update_view(request, object_id=None):
    product = get_object_or_404(Product, pk=object_id)
    form = ProductModelForm(request.POST or None, instance=product)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    template = "products/form.html"
    context = {'object': product,
               'form': form,
               "submit_btn": "Update Product",
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
    context = {'queryset':queryset}
    return render(request, template, context)

# ****************************************************************************************************
