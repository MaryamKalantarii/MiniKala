from rest_framework import serializers
from ...models import ProductModel,ProductCategoryModel

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategoryModel
        fields = ["id", "title","slug"]

class ProductSerializer(serializers.ModelSerializer):

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
        ]
        read_only_fields = ['created_date', 'updated_date', 'avg_rate']
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['category'] = CategorySerializer(instance.category, many=True).data
        return rep
        

