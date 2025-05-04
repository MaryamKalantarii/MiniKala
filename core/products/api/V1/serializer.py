from rest_framework import serializers
from ...models import ProductModel,ProductCategoryModel
from accounts.api.V1.serializer import UserMiniSerializer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategoryModel
        fields = ["id", "title","slug"]

class ProductSerializer(serializers.ModelSerializer):
    
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
            'detail_link',  
        ]
        read_only_fields = ['created_date', 'updated_date', 'avg_rate','user']

   
    def get_detail_link(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/V1/products/{obj.slug}/')
        return None

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = UserMiniSerializer(instance.user).data
        rep['category'] = CategorySerializer(instance.category.all(), many=True).data
        return rep