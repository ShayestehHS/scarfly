from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import APIException, NotFound, ValidationError

from orders.models import Coupon, Order
from orders.utils import calculate_pay_amount, get_authority, verify
from products.models import Product


class RetrieveOrderSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, obj: Order):
        product = self.context.get('product')
        if product is None:
            product = Product.objects.filter(id=obj.product_id).only('name').first()

        data = {'id': obj.product_id, 'name': product.name}
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


class OrderCreateSerializer(serializers.ModelSerializer):
    product = serializers.CharField()

    class Meta:
        model = Order
        fields = ('product', 'address', 'postal_code', 'offer_key')

    def validate_product(self, value):
        product = Product.objects.filter(pro_code=value).only('sell_price', 'id', 'pro_code').first()
        if product is None:
            raise NotFound({'product': 'Not found'})
        return product

    def validate_offer_key(self, value):
        coupon = Coupon.objects.filter(key__exact=value).first()
        if coupon is None:
            raise NotFound({'offer_key': "Not found"})
        return coupon

    def to_representation(self, instance):
        context = self.context.copy()
        context['product'] = self.validated_data['product']
        return UpdateOrderStatusSerializer(instance=instance, context=context).data

    def create(self, validated_data):
        product: Product = validated_data['product']
        request = self.context['request']
        user = request.user
        description = self.context.get('description', "خرید از: اسکارف‌لی")
        pay_amount = calculate_pay_amount(coupon=validated_data.get('offer_key'), sum_product_price=product.sell_price)

        authority = get_authority(pay_amount, description, user.phone_number, user.email)
        try:
            order = Order.objects.create(user=user, product_id=product.id, address=validated_data['address'],
                                         offer_key=validated_data.get('offer_key'), pay_amount=pay_amount,
                                         authority=authority, postal_code=validated_data['postal_code'])
        except IntegrityError as e:
            raise APIException({"duplicated": e.message})

        return order
