import os
from django.conf import settings

# guess the file type
from mimetypes import guess_type

# Q Lookups: a bit more advanced search
from django.db.models import Q, Avg, Count

# file wrapper (ver se nao tem uma forma mais decente de
# fornecer isso ( pelo que me parece foi deprecado ou mudou de pacote ) )
from wsgiref.util import FileWrapper

from django.shortcuts import render
# Create your views here.
from .forms import ProductAddForm, ProductModelForm
from .models import Product, ProductRating, MyProducts

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from django.http import JsonResponse
from django.views.generic import View

# ------------------------ CLASS BASED VIEWS ------------------------
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
# -------------------------------------------------------------------
from digitalmarket.mixins import MultiSlugMixin, SubmitBtnMixin, LoginRequiredMixin, AjaxRequiredMixin
from .mixins import ProductManagerMixin

from sellers.models import SellerAccount
from sellers.mixins import SellerAccountMixin
from tags.models import Tag
# verificar se pode importar assim (mesmo tipo de import esta em products/templatetags/get_thumbnail.pys

from django.core.urlresolvers import reverse

from analytics.models import TagView


# ************************************* CLASS BASED VIEWS ********************************************

class ProductRatingAjaxView(AjaxRequiredMixin, View):
    """
    Quando printa no console do javascript erro 500 pode ser problema com o codigo
    1: checar o spacing (as vezes o ajax acusa erro doido mas na verdade so precisa ajeitar espacamento)
    2: checar os try-except e se as get calls dos objetos estao funcionando

    """
    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated():
            return JsonResponse({}, status=401)

        user = request.user
        product_id = request.POST.get("product_id")
        rating_value = request.POST.get("rating_value")
        product_obj = Product.objects.filter(id=product_id).first()
        if not product_obj:
            return JsonResponse({}, status=404)

        try:
            product_obj = Product.objects.get(id=product_id)
        except:
            product_obj = Product.objects.filter(id=product_id).first()

        rating_obj, rating_obj_created = ProductRating.objects.get_or_create(
            user=user,
            products=product_obj
        )

        """MANEIRA ESTUPIDA!!!!!! MTAS CONSULTAS AO BANCO!!!"""
        try:
            rating_obj = ProductRating.objects.get(user=user, products=product_obj)
        except ProductRating.MultipleObjectsReturned:
            rating_obj = ProductRating.objects.filter(user=user, products=product_obj).first()
        except:
            # uma maneira de fazer
            # rating_obj = ProductRating.objects.create(user=user, product=product_obj)
            # outra
            rating_obj = ProductRating()
            rating_obj.user = user
            rating_obj.products = product_obj
        rating_obj.rating = int(rating_value)

        # verify ownership (podia memo é nao mostrar as estrelinhas caso o cara nao seja autenticado
        # reverse relationship
        myproducts = user.myproducts.products.all()
        if product_obj in myproducts:
            rating_obj.verified = True
        rating_obj.save()

        data = {
            "success": True
        }
        return JsonResponse(data)


class ProductCreateView(SellerAccountMixin, SubmitBtnMixin, CreateView):
    model = Product
    form_class = ProductModelForm
    template_name = "products/form.html"
    # success_url = "/product/list"
    submit_btn = "Add Product"

    def form_valid(self, form):
        # user = self.request.user
        # form.instance.user = user
        seller = self.get_account()
        form.instance.seller = seller
        valid_data = super(ProductCreateView, self).form_valid(form)
        tags = form.cleaned_data.get("tags")
        # solucao porca! apaga todas as tags relacionadas e insere de novo no banco o novo set de tags
        # mesmo se for repetido
        # talvez tenha algum caso q falhe!!! rever
        if tags:
            tag_list = tags.split(",")
            for tag in tag_list:
                tag = ''.join(tag.split(" "))
                if not tag == " " and not tag == "":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.products.add(form.instance)
        return valid_data

    # just showing that I can use reverse in this function as well
    # def get_success_url(self):
    #     return reverse("products:list")


class ProductDetailView(MultiSlugMixin, DetailView):
    model = Product

    def get_context_data(self, *args,**kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        tags = obj.tag_set.all()
        # +*+*+*+*+*+*+*+*codigo criado para determinar a hora de mostrar as votacao do produto ou nao+*+*+*+*+*+*+*
        user = str(obj.seller)
        logged_user = str(self.request.user)
        context['is_owner'] = False
        # nao vai mostrar as estrelinhas se o cara for o dono do produto ou se ele nao estiver logado
        if user == logged_user or not self.request.user.is_authenticated():
            context['is_owner'] = True

        # ----------------------------------------------------------------------------------------------------------
        rating_avg = obj.productrating_set.aggregate(Avg('rating'), Count('rating'))
        context['rating_avg'] = rating_avg
        if self.request.user.is_authenticated():
            # getting star rate
            rating_obj = ProductRating.objects.filter(user=self.request.user, products=obj)
            if rating_obj.exists():
                context['my_rating'] = rating_obj.first().rating
            for tag in tags:
                new_view = TagView.objects.add_count(self.request.user, tag)
                # new_view = TagView.objects.get_or_create(
                #     user=self.request.user,
                #     tag=tag
                # )[0]
                # new_view.count += 1
                # new_view.save()

        return context


class ProductDownloadView(MultiSlugMixin, DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        # download permissions
        if obj in request.user.myproducts.products.all():
            filepath = os.path.join(settings.PROTECTED_ROOT, obj.media.path)
            guessed_type = guess_type(filepath)[0]
            wrapper = FileWrapper(open(filepath, 'rb'))
            mimetype = 'application/force-download'
            if guessed_type:
                mimetype = guessed_type

            response = HttpResponse(wrapper, content_type=mimetype)
            if not request.GET.get("preview"):
                response["Content-Disposition"] = "attachment; filename=%s" % obj.media.name

            # related to different type of servers
            response["X-SendFile"] = str(obj.media.name)
            return response
        else:
            raise Http404


class SellerProductListView(SellerAccountMixin, ListView):
    model = Product
    template_name = 'sellers/product_list_view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super(SellerProductListView, self).get_queryset(*args)
        qs = qs.filter(seller=self.get_account())
        query = self.request.GET.get("q")
        # gambi pra funcionar
        if not query:
            query = ""
        qs = qs.filter(Q(title__icontains=query) |
                       Q(description__icontains=query)).order_by("title")
        return qs


class VendorListView(ListView):
    model = Product
    template_name = "products/product_list.html"

    def get_object(self):
        username = self.kwargs['vendor_name']        # seller has a foreign key to user that has a field username
        seller = get_object_or_404(SellerAccount, user__username=username)
        return seller

    def get_context_data(self, *args,**kwargs):
        # TESTE... SE ALGO DER ERRADO COM ISSO AQUI ADICIONAR *args antes de **kwargs abaixo
        context = super(VendorListView, self).get_context_data(**kwargs)
        context['vendor_name'] = str(self.get_object().user.username)
        return context

    def get_queryset(self, *args, **kwargs):
        seller = self.get_object()
        qs = super(VendorListView, self).get_queryset(*args).filter(seller=seller)
        query = self.request.GET.get("q")
        if not query:
            query = ""
        qs = qs.filter(Q(title__icontains=query) |
                       Q(description__icontains=query)).order_by("title")
        return qs


class ProductListView(ListView):
    model = Product
    # template_name = "products/list_view.html"
    #
    # def get_context_data(self, **kwargs):
    #     context = super(ProductListView, self).get_context_data(**kwargs)
    #     context["queryset"] = self.get_queryset()
    #     return context

    def get_queryset(self, *args, **kwargs):
        # ATENCAO! TROQUEI **KWARGS PARA *ARGS NA LINHA ABAIXO (FAZENDO FUNCIONAR PRA PYTHON3.X)
        # NAO SEI O PQ DISSO.
        qs = super(ProductListView, self).get_queryset(*args)
        query = self.request.GET.get("q")
        # gambi pra funcionar
        if not query:
            query = ""
        qs = qs.filter(Q(title__icontains=query) |
                       Q(description__icontains=query)).order_by("title")
        return qs


class UserLibraryListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "products/library_list.html"

    def get_queryset(self, *args, **kwargs):
        obj = MyProducts.objects.get_or_create(user=self.request.user)[0]
        qs = obj.products.all()
        query = self.request.GET.get("q")
        # gambi pra funcionar
        if not query:
            query = ""
        qs = qs.filter(Q(title__icontains=query) |
                       Q(description__icontains=query)).order_by("title")
        return qs


class ProductUpdateView(ProductManagerMixin, SubmitBtnMixin, MultiSlugMixin, UpdateView):
    model = Product
    form_class = ProductModelForm
    template_name = "products/form.html"
    # success_url = "/seller/product/"
    submit_btn = "Update Product"

    def get_initial(self):
        initial = super(ProductUpdateView, self).get_initial()
        tags = self.get_object().tag_set.all()
        initial["tags"] = ", ".join([x.title for x in tags])
        """
        Same thing as:
        tag_list = []
        for x in tags:
            tag_list.append(x.title)
        """
        return initial

    def form_valid(self, form):
        valid_data = super(ProductUpdateView, self).form_valid(form)
        tags = form.cleaned_data.get("tags")
        obj = self.get_object()
        # solucao porca! apaga todas as tags relacionadas e insere de novo no banco o novo set de tags
        # mesmo se for repetido
        # talvez tenha algum caso q falhe!!! rever
        obj.tag_set.clear()
        if tags:
            tag_list = tags.split(",")
            for tag in tag_list:
                tag = ''.join(tag.split(" "))
                print(tag)
                if not tag == " " and not tag == "":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.products.add(obj)
        return valid_data

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
    # Easy way to create forms
    form = ProductModelForm(request.POST or None, request.FILES or None)
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
