from __future__ import unicode_literals
from django.db import models
from usercenter import config
from usercenter.storage import *

# 用户信息
# 变量名称太奇怪了，我改一下
class UserInfo(models.Model):
    uname = models.CharField(max_length=30)
    upassword = models.CharField(max_length=20)
    uemail = models.CharField(max_length=30)
    uphonenumber = models.CharField(max_length=15)
    uregDate = models.DateTimeField(auto_now_add=True)
    isactive = models.BooleanField(default=False)

    def __str__(self):
        return self.uName


# 订单地址
class AddrInfo(models.Model):
    addressid = models.IntegerField(default=0)
    phonenumber = models.CharField(max_length=30)
    recipname = models.CharField(max_length=30)
    detaaddress = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10, default='')
    user = models.ForeignKey('UserInfo', related_name='addrinfos')

    def __str__(self):
        return self.detaaddress


# 购物车
class Cart(models.Model):
    goodsid = models.ForeignKey('Goods', related_name='carts')
    buycount = models.IntegerField(default=1)
    user = models.ForeignKey('UserInfo', related_name='carts')

    def __str__(self):
        return self.goodsName


# 订单
class Orders(models.Model):
    isFinish = models.BooleanField(default=False)
    isDelete = models.BooleanField(default=False)
    orderTime = models.DateTimeField()
    orderNumber = models.CharField(max_length=20, null=True, blank=True)
    addr = models.IntegerField(null=True, blank=True)
    userOrder = models.ForeignKey('UserInfo', related_name='orders')

    def __str__(self):
        return self.addr


# 订单里的一件商品信息
class OrderDetail(models.Model):
    goodName = models.CharField(max_length=30)
    goodPrice = models.DecimalField(max_digits=10, decimal_places=2)
    buyCount = models.IntegerField()
    orders_id = models.ForeignKey('Orders', related_name='orderdetails')
    good_id = models.ForeignKey('Goods', related_name='orderdetails')

    def __str__(self):
        return self.goodName


class GoodSort(models.Model):
    sortid = models.IntegerField(default=0)
    sortname = models.CharField(max_length=20)
    sortimg = models.ImageField(u"图片", upload_to='image', default=None, storage=ImageStorage())
    sortdesc = models.TextField()

    def get_abstract(self):
        intro = {
            'id': self.sortid,
            'img': "{proto}://{domain}{path}".format(
                proto=config.PROTOCOL,
                domain=config.DOMAIN,
                path=self.img.url,
            ),
            'name': self.sortname,
            'sec': self.sortdesc,
        }
        return intro

    def get_goodjson(self):
        intro = []
        for obj in self.goods.all():
            intro.append(obj.get_abstract(False))
        return intro

    def __str__(self):
        return self.sortname


# 商品，以自改
class Goods(models.Model):
    goodsort = models.ForeignKey('GoodSort', related_name='goods')
    goodname = models.CharField(u'商品名', max_length=30)
    gooddesc = models.CharField(u'商品介绍', max_length=80)
    goodprice = models.DecimalField(u'商品价格', max_digits=7, decimal_places=2)
    img = models.ImageField(u"图片", upload_to='image', default=None, storage=ImageStorage())
    salecount = models.IntegerField(u'销量', default=0)
    stockcount = models.IntegerField(u'库存', default=0)
    copa = models.ForeignKey('Copa', related_name='goods')
    gupdate = models.DateTimeField()

    def get_abstract(self, verbose):
        intro = {
            'id': self.id,
            'img_url': "{proto}://{domain}{path}".format(
                proto=config.PROTOCOL,
                domain=config.DOMAIN,
                path=self.img.url,
            ),
            'name': self.goodname,
            'copa_name': self.copa.copaname,
            'inform': self.gooddesc,
        }
        if verbose == 'detial':
            intro['salecount'] = self.salecount
            intro['stockcount'] = self.stockcount
            intro['price'] = self.goodprice,
            intro['copasec'] = self.copa.copasec,
        return intro

    def save(self, *args, **kwargs):
        super(Goods, self).save(*args, **kwargs)

    def __str__(self):
        return self.goodname

    class Meta:
        verbose_name = u'商品'
        verbose_name_plural = verbose_name


class Copa(models.Model):
    copaname = models.CharField(u'合作社名称', max_length=30)
    copasec = models.CharField(u'合作社介绍', max_length=80)
    copaadd = models.CharField(u'合作社地址', max_length=80, default=None)

    def __str__(self):
        return self.copaname


class index_img(models.Model):
    imgname = models.CharField(u'轮播图名称', max_length=30)
    img = models.ImageField(u"图片", upload_to='image', default=None, storage=ImageStorage())

    def get_abstract(self):  # 把图片以字典的形式返回
        intro = {
            'id': self.id,
            'img': "{proto}://{domain}{path}".format(
                proto=config.PROTOCOL,
                domain=config.DOMAIN,
                path=self.img.url,
            ),
            'name': self.imgname,
        }
        return intro

    def __str__(self):
        return self.imgname


