from rest_framework import serializers
from ...models import ProductModel,ProductCategoryModel

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategoryModel
        fields = ["id", "title","slug"]

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    detail_link = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = [
            'id',
            'user',
            'category',
            'title',
            'slug',
            'image',
            'description',
            'brief_description',
            'stock',
            'price',
            'discount_percent',
            'avg_rate',
            'created_date',
            'updated_date',
            'is_discounted',
            'is_published',
            'detail_link',  # 🔗 این خط
        ]
        read_only_fields = ['created_date', 'updated_date', 'avg_rate']

    def get_category(self, obj):
        return CategorySerializer(obj.category.all(), many=True).data

    def get_detail_link(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/V1/products/{obj.slug}/')
        return None
