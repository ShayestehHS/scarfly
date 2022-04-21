from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import APIException

from orders.models import Order
from orders.utils import get_authority
from products.models import Product


class OrderDetailUpdateSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, obj: Order):
        product = self.context.get('product')
        if product is None:
            product = Product.objects.filter(id=obj.product_id).only('name').first()

        data = {'id': obj.product_id, 'name': product.name}
        return data

    class Meta:
        model = Order
        fields = ('product', 'address', 'postal_code', 'authority', 'payment_id', 'status', 'offer_key', 'timestamp')
        read_only_fields = ('is_paid', 'authority')


class OrderCreateSerializer(serializers.ModelSerializer):
    product = serializers.CharField()

    class Meta:
        model = Order
        fields = ('product', 'address', 'postal_code')

    def validate_product(self, value):
        product = Product.objects.filter(pro_code=value).only('sell_price', 'id', 'pro_code').first()
        if product is None:
            raise serializers.ValidationError({'product': 'Please enter a valid product code.'})
        return product

    def to_representation(self, instance):
        context = self.context.copy()
        context['product'] = self.validated_data['product']
        return OrderDetailUpdateSerializer(instance=instance, context=context).data

    def create(self, validated_data):
        product: Product = validated_data['product']
        request = self.context['request']
        user = request.user
        description = self.context.get('description', "خرید از: اسکارف‌لی")

        authority = get_authority(product.sell_price, description, user.phone_number, user.email)
        try:
            order = Order.objects.create(user=user, product_id=product.id, address=validated_data['address'],
                                         authority=authority, postal_code=validated_data['postal_code'])
        except IntegrityError as e:
            raise APIException({"duplicated": e.message})

        return order
