from __future__ import annotations
from ast import Or
from itertools import count, product
from multiprocessing.sharedctypes import Value
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value, FloatField, Func, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from store.models import Product, Customer, Collection, Order, OrderItem, Collection
from tags.models import TaggedItem

def say_hello(request):
    content_type = ContentType.objects.get_for_model(Product)
    queryset = TaggedItem.objects.select_related('tag').filter(
        content_type=content_type,
        object_id=1
    )

    return render(request, 'hello.html', {
        'name': 'Mustafa',
        'orders': queryset
    })
