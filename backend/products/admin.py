from django.contrib import admin
from django.forms import TextInput
from django.db import models
from django.utils.html import format_html

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def image_tag(self, obj: Product):
        return format_html(f'<img src="{obj.image.url}" with=100 height=100/>')

    @admin.action(description='Mark selected products as paid to provider')
    def make_paid(modeladmin, request, queryset):
        queryset.update(is_paid_to_provider=True)

    @admin.action(description='Mark selected products as not available')
    def make_not_available(modeladmin, request, queryset):
        queryset.update(is_available=False)

    list_display = ('image_tag', 'pro_code', 'name', 'sell_price', 'is_available')
    list_display_links = ('image_tag',)
    list_filter = ('is_available',)
    search_fields = ('pro_code', 'name')
    search_help_text = "Search by product code or name of products."
    list_per_page = 20
    ordering = ('-pro_code',)
    actions = ['make_paid', 'make_not_available']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'autocomplete': 'off', 'class': 'vTextField'})},
        models.IntegerField: {'widget': TextInput(attrs={'autocomplete': 'off', 'class': 'vIntegerField'})},
    }
    fields = (
        ('name', 'pro_code'),
        'image', 'channel_message_id',
        'instagram_url',
        ('sell_price', 'buy_price'),
        ('is_available',),
        'description',
    )
