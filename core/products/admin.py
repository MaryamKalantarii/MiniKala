from django.contrib import admin
from .models import ProductModel, ProductCategoryModel

@admin.register(ProductCategoryModel)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_date']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_date']

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'user_email', 'status', 'price', 'discount_percent', 'stock', 'is_discounted', 'is_published', 'created_date']
    list_filter = ['status', 'category', 'created_date']
    search_fields = ['title', 'description', 'slug']
    readonly_fields = ['created_date', 'updated_date', 'avg_rate']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['category']

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def is_discounted(self, obj):
        return obj.is_discounted()
    is_discounted.boolean = True

    def is_published(self, obj):
        return obj.is_published()
    is_published.boolean = True
