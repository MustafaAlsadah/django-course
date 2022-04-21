from cgitb import html
from turtle import title
from django.contrib import admin
from . import models
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

# Register your models here.
class number_of_orders_filter(admin.SimpleListFilter):
    '''
    Special `filter for customers` that filters them based on the number of orders they have placed
    '''
    title = 'number of orders'
    parameter_name = 'number of orders'

    def lookups(self, request, model_admin):
        return [
            ('>=2', 'moderate'),
            ('>=4', 'premium'),
            ('>=6', 'exceptional') 
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '>=2':
            return queryset.filter(number_of_orders__gte=2)
        elif self.value() == '>=4':
            return queryset.filter(number_of_orders__gte=4)
        elif self.value() == '>=6':
            return queryset.filter(number_of_orders__gte=6)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory<10:
            return 'Low'
        else:
            return 'OK'
    

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'number_of_orders']
    list_editable = ['membership']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_filter = ['membership', number_of_orders_filter]

    @admin.display(ordering='number_of_orders')
    def number_of_orders(self, customer):
        url = (reverse('admin:store_order_changelist')
               +'?'
               +urlencode({
                   'customer__pk':str(customer.pk)
               }))
        return format_html('<a href="{}">{}</a>', url, customer.number_of_orders)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            number_of_orders = Count('order')
        )

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'placed_at', 'customer']

    @admin.display(ordering='pk')
    def order_id(self, order):
        return order.pk

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        url = (reverse('admin:store_product_changelist')
              + '?'
              + urlencode({
                  'collection__id':str(collection.id)
              }))
        return format_html('<a href="{}">{}</a>',url ,collection.product_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count = Count('product')
        )