from django.contrib import admin

# Register your models here.
from .models import (Product,
                     MyProducts,
                     Thumbnail,
                     ProductRating,
                     CuratedProducts
                     )

# show more information on admin page of products
# how stuff render or how stuff looks


class ThumbnailInLine(admin.TabularInline):
    extra = 1
    model = Thumbnail


class ProductAdmin(admin.ModelAdmin):
    inlines = [ThumbnailInLine]
    list_display = ["__str__", "description", "price", "sale_price"]
    search_fields = ["title", "description"]
    list_filter = ["price", "sale_price"]
    list_editable = ["sale_price"]
    # prepopulated_fields = {"slug": ("title")}

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(MyProducts)
admin.site.register(Thumbnail)
admin.site.register(ProductRating)
admin.site.register(CuratedProducts)


