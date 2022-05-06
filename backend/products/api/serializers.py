from rest_framework import serializers

from products.models import Product


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('pk', 'name', 'image', 'pro_code', 'sell_price', 'description')


class ListProductSerializer(ProductDetailSerializer):
    pass
