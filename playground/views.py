from itertools import product
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
from store.models import Product, Customer, Collection, Order, OrderItem

def say_hello(request):
    product_queryset = Product.objects.filter(
        Q(orderitem__product_id=F('id'))
        ).distinct().order_by('title')

    return render(request, 'hello.html', {
        'name': 'Mustafa',
        'products':list(product_queryset)
    })
