from django.contrib import admin
from django.db import models
from django.db.models import Count
from django.utils.html import format_html,urlencode
from django.urls import reverse
from . import models

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>=10', 'OK')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        if self.value() == '>=10':
            return queryset.filter(inventory__gte=10)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'last_update','get_collection']
    list_editable = ['unit_price']
    search_fields=['title__istartswith']
    list_filter = ['collection','last_update',InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    ordering=['inventory']


    def get_collection(self,product):
        return product.collection.title
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    ordering=['first_name','last_name']
    list_display=['first_name','last_name','email','phone','membership']
    list_editable=['membership']
    list_per_page=15

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'orderitem_product', 'placed_at', 'customer', 'payment_status']
    list_per_page = 15

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related('customer')
            .prefetch_related('orderitem_set__product')
        )

    @admin.display(ordering='orderitem__product__title')
    def orderitem_product(self, order):
        items = order.orderitem_set.all()  # already prefetched
        titles = [item.product.title for item in items]
        return ", ".join(titles) or "-"


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display=['title',"products_count"]
    # list_select_related=['product_set']

    def products_count(self,collection):
        url=reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id': str(collection.id)})
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )