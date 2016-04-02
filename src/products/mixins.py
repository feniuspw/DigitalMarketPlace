from django.http import Http404

from sellers.mixins import SellerAccountMixin


class ProductManagerMixin(SellerAccountMixin, object):

        def get_object(self, *args, **kwargs):
            seller = self.get_account()
            obj = super(ProductManagerMixin, self).get_object(*args, **kwargs)

            # Creio que nao preciso disso aqui embaixo, mas vou deixar caso de algum pau
            # try:
            #     obj.seller == seller
            # except:
            #     raise Http404

            if obj.seller == seller:
                return obj
            else:
                raise Http404
