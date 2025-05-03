from django.contrib import admin
from .models import ProductModel,ProductCategoryModel
# Register your models here.

admin.site.register(ProductModel)
admin.site.register(ProductCategoryModel)