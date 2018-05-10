from django.shortcuts import render, redirect
from usercenter.models import *
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from usercenter.utils import UploadMediaManager
from .islogin import islogin
from django.db import transaction


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

# 返回该用户的购物车信息
#@islogin
def view_cart(request):
    cart_list = []
    #uid = request.session['user_id']
    uid = 1
    user = UserInfo.objects.get(id=uid)
    carts = user.carts.all()
    for obj in carts.order_by('id'):
        cart_list.append(obj.get_abstract())
    return JsonResponse({'error': 0, 'cart_list': cart_list})


# 添加购物车
#@islogin
def add_cart(request, gid, count):
    #uid = request.session['user_id']
    uid = 1
    gid = int(gid)
    count = int(count)
    # 查询购物车是否已经有此商品，有则增加
    carts = Cart.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count + count
    else:
        user = UserInfo.objects.get(id=uid)
        good = Goods.objects.get(id=gid)
        cart = Cart()
        cart.user = user
        cart.goods = good
        cart.buycount = count
    cart.save()
    return redirect('/cart/')


# 编辑购物车
#@islogin
def edit_cart(request, cart_id, count):
    try:
        cart = Cart.objects.get(id=int(cart_id))
        count1 = cart.buycount = int(count)
        cart.save()
        data = {'ok': 0}
    except Exception as e:
        data = {'ok': count1}
    return JsonResponse(data)

#删除购物车
#@islogin
def delete_cart(request, cart_id):
    cart = Cart.objects.get(id=int(cart_id))
    cart.delete()


#@islogin
@transaction.atomic()
def order_handle(request):
    # 保存一个事物点
    tran_id = transaction.savepoing()
    try:
        post = request.POST
        orderlist = post.getlist('id[]')
        total = post.get('total')
        address = post.get('address')

        order = Orders()
        now = datetime.now()
        uid = request.session.get('user_id')
        user = UserInfo.objects.get(id=uid)
        order.oid = '{}{}'.format(now.strftime('%Y%m%d%H%M%S').uid)
        order.user = user
        order.orderTime = now
        order.ototal = Decimal(total)
        order.addr = address
        order.save()

        #遍历购物车中提交的信息，创建订单详情表
        for orderid in orderlist:
            cart = Cart.objects.get(id=orderid)
            good = cart.goods
            if int(good.stockcount) >= int(cart.buycount):
                good.stockcount -= int(cartinfo.count)
                good.save()


                orderdetail = OrderDetail()
                orderdetail.goods = good
                orderdetail.orders = order
                orderdetail.price = Decimal(int(goodiprice))
                orderdetail.count = int(cart.buycount)
                orderdetail.save()

                cart.delete()
            else:
                # 库存不够发出事务回滚
                transaction.savepoint_rollback(tran_id)
                #返回json供前台提示失败
                return JsonResponse({'status': 2})

    except Exception as e:
        transaction.savepoint_rollback(tran_id)
    return JsonResponse({'status': 1})
