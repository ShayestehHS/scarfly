from django.contrib import admin, messages
from orders.models import Order, Coupon


def start_getting_product(modeladmin, request, queryset):
    for order in queryset:
        if order.status != '2':
            messages.error(request, f"Invalid order status for {order.product}")
            return
    queryset.update(status='3')
    messages.success(request, f"{len(queryset)} orders are updated")


start_getting_product.short_description = 'Start to getting products'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_id', 'status')
    readonly_fields = ('id',)
    actions = [start_getting_product]


@admin.register(Coupon)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = (
        'id',
        ('offer_amount', 'is_percent'),
        'key',
        'expire_date',
        'description',
    )
