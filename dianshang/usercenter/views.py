from django.shortcuts import render
from usercenter.models import *
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST


@require_GET
def view_good_list(request):
    content = []
    for obj in Goods.objects.order_by('goodsort'):
        content.append(obj.get_abstract('detial'))
    return JsonResponse({'error': 0, 'content': content})


@require_GET
def view_good_detial(request, id):
    obj = Goods.objects.get(id=id)
    content = obj.get_abstract('detial')
    return JsonResponse({'error': 0, 'content': content})

# view_index 返回首页需要的json数据
@require_GET
def view_index(request):
    img_list = []
    good_list = []
    for obj in index_img.objects.order_by('id'):
        img_list.append(obj.get_abstract())

    for obj_2 in GoodSort.objects.order_by('id'):
        good_list.append(obj_2.get_goodjson())

    return JsonResponse({'error': 1, 'banner': img_list, 'goods': good_list})
