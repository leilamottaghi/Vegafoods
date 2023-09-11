from django.contrib import admin
from .models import ProductImageModel,CategoryModel,BlogModel,ProductModel, ContactModel,PurchaseInvoice


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    pass


@admin.register(PurchaseInvoice)
# class ProductImageModelAdmin(admin.ModelAdmin):
#     pass

@admin.register(ProductImageModel)
class ProductImageModelAdmin(admin.ModelAdmin):
    pass

@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    pass

@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    pass


@admin.register(BlogModel)
class BlogModelAdmin(admin.ModelAdmin):
    pass



