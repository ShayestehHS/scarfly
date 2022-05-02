from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import APIException, NotFound, ValidationError

from orders.models import Coupon, Order
from orders.utils import verify
from products.models import Product


class RetrieveOrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, obj: Order):
        products = self.context.get('products')
        if products is None:
            products = obj.products.only('id', 'name', 'pro_code')

        data = []
        for product in products:
            data.append({'id': product.id, 'name': product.name,
                         'pro_code': product.pro_code})
        return data

    class Meta:
        model = Order
        exclude = ('user', 'tracking_code', 'is_paid_to_provider')
        read_only_fields = ('is_paid', 'authority')


class UpdateOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status',)

    def update(self, instance: Order, validated_data):
        is_paid = verify(instance.authority, instance.pay_amount)
        if not is_paid:
            raise ValidationError({'detail': 'Error in validating the authority code'})
        return super(UpdateOrderStatusSerializer, self).update(instance, validated_data)


class CreateOrderSerializer(serializers.ModelSerializer):
    products = serializers.ListSerializer(child=serializers.IntegerField())
    postal_code = serializers.CharField(min_length=10, max_length=10, allow_null=True, allow_blank=True)

    class Meta:
        model = Order
        fields = ('products', 'address', 'postal_code', 'offer_key')

    def validate_products(self, value):
        products = Product.objects.filter(pro_code__in=value) \
            .only('sell_price', 'id', 'pro_code', 'name')
        if len(products) == 0:
            raise NotFound({'products': 'Not found'})
        return products

    def validate_offer_key(self, value):
        if not value:
            return None
        coupon = Coupon.objects.filter(key__exact=value).first()
        if coupon is None:
            raise NotFound({'offer_key': "Not found"})
        return coupon

    def to_representation(self, instance):
        context = self.context.copy()
        context['products'] = self.validated_data['products']
        return RetrieveOrderSerializer(instance=instance, context=context).data

    def create(self, validated_data):
        products = validated_data['products']
        request = self.context['request']
        user = request.user

        try:
            order = Order.objects.create(user=user, address=validated_data['address'],
                                         offer_key=validated_data.get('offer_key'),
                                         postal_code=validated_data['postal_code'])
        except IntegrityError as e:
            raise APIException({"duplicated": e.message})

        order.products.add(*products)
        return order


class ListOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('user', 'is_paid_to_provider', 'offer_key')
