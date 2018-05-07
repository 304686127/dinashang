from django.shortcuts import render
from usercenter.models import *
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from usercenter.utils import UploadMediaManager


# 上传图片
@require_POST
def upload_media(request):
    media_type = request.GET.get('dir')
    media_data = request.FILES.get('file')
    manager = UploadMediaManager()
    media_url = manager.save(media_type, media_data)
    return JsonResponse({'error': 1, 'url': media_url})


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
    # 这里把error改成0
    return JsonResponse({'error': 0, 'banner': img_list, 'goods': good_list})


# 注册，成功后跳转到邮箱验证
@require_POST
def sign_up(request):
    if request.user.is_authenticated():
        return JsonResponse({'error': 1, 'number': '1101', 'detail': 'have log in'})
    if request.method == 'POST':
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        email = request.POST.get('email', ''),
        phonenumber = request.POST.get('phonenumber', '')
        if password == '' or repeat_password == '':
            return JsonResponse({'error': 1, 'number': '1102', 'detail': 'no password'})
        elif password != repeat_password:
            return JsonResponse({'error': 1, 'number': '1103', 'detail': 'password not same'})
        elif email == '':
            return JsonResponse({'error': 1, 'number': '1105', 'detail': 'no email'})
        else:
            username = request.POST.get('username', '')
            if UserInfo.objects.filter(username=username):
                return JsonResponse({'error': 1, 'number': '1104', 'detail': 'name used'})
            else:
                new_user = UserInfo.objects.create_user(uname=username, upassword=password,
                                                        uemail=email,
                                                        uphonenumber=phonenumber, )
                new_user.isactive = False
                new_user.save()
                return JsonResponse({'error': 0})
