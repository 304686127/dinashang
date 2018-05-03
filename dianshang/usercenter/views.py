from django.shortcuts import render
from usercenter.models import *
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST


@require_GET
def view_good_list(request):
    content = []
    for obj in Goods.objects.order_by('goodsort'):
        content.append(obj.get_abstract())
    return JsonResponse({'error': 0, 'content': content})


@require_GET
def view_good_detial(request, id):
    obj = Goods.objects.get(id=id)
    content = obj.get_abstract('detial')
    return JsonResponse({'error': 0, 'content': content})
