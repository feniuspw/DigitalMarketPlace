from django.contrib import admin

# Register your models here.
from .models import Product

# show more information on admin page of products
# how stuff render or how stuff looks


class ProductAdmin(admin.ModelAdmin):
    list_display = ["__str__", "description", "price", "sale_price"]
    search_fields = ["title", "description"]
    list_filter = ["price", "sale_price"]
    list_editable = ["sale_price"]

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)



