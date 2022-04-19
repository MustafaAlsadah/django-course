from __future__ import annotations
from ast import Or
from hashlib import new
from imp import get_tag
from itertools import count, product
from multiprocessing.sharedctypes import Value
from turtle import title
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value, FloatField, Func, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from store.models import Cart, CartItem, Product, Customer, Collection, Order, OrderItem, Collection
from tags.models import TaggedItem
from django.db import transaction

def say_hello(request):
    with transaction.atomic():
        order = Order()
        order.customer_id = 87
        order.payment_status = 'C'
        order.save()

        orderitem = OrderItem()
        orderitem.order = order
        orderitem.product_id = -1
        orderitem.unit_price = 11
        orderitem.quantity = 3
        orderitem.save()

        queryset = Order.objects.all()

        return render(request, 'hello.html', {
            'name': 'Mustafa',
            'orders': queryset
        })
