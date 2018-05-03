from __future__ import unicode_literals
from django.db import models
from usercenter import config
from usercenter.storage import *


# 用户信息
class UserInfo(models.Model):
    uName = models.CharField(max_length=30)
    uPassword = models.CharField(max_length=20)
    uEmail = models.CharField(max_length=30)
    uPhoneNumber = models.CharField(max_length=15)
    uRegDate = models.DateTimeField(auto_now_add=True)
    isactive = models.BooleanField(default=False)

    def __unicode__(self):
        return self.uName


# 订单地址
class AddrInfo(models.Model):
    addressid = models.IntegerField(default=0)
    phonenumber = models.CharField(max_length=30)
    recipname = models.CharField(max_length=30)
    detaaddress = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10, default='')
    user = models.ForeignKey('UserInfo')

    def __str__(self):
        return self.detaaddress.encode('utf-8')


# 购物车
class Cart(models.Model):
    goodsid = models.ForeignKey('Goods')
    buycount = models.IntegerField(default=1)
    user = models.ForeignKey('UserInfo')

    def __str__(self):
        return self.goodsName.encode('utf-8')


# 订单
class Orders(models.Model):
    isFinish = models.BooleanField(default=False)
    isDelete = models.BooleanField(default=False)
    orderTime = models.DateTimeField()
    orderNumber = models.CharField(max_length=20, null=True, blank=True)
    addr = models.IntegerField(null=True, blank=True)
    userOrder = models.ForeignKey('UserInfo')

    def __str__(self):
        return self.addr.encode('utf-8')


# 订单里的一件商品信息
class OrderDetail(models.Model):
    goodName = models.CharField(max_length=30)
    goodPrice = models.DecimalField(max_digits=10, decimal_places=2)
    buyCount = models.IntegerField()
    orders_id = models.ForeignKey('Orders')
    good_id = models.ForeignKey('Goods')

    def __str__(self):
        return self.goodName.encode('utf-8')


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


# 商品，以自改
class Goods(models.Model):
    goodsort = models.ForeignKey(u'商品分类', 'GoodSort')
    goodname = models.CharField(u'商品名', max_length=30)
    gooddesc = models.CharField(u'商品介绍', max_length=80)
    goodprice = models.DecimalField(u'商品价格', max_digits=7, decimal_places=2)
    img = models.ImageField(u"图片", upload_to='image', default=None, storage=ImageStorage())
    salecount = models.IntegerField(u'销量', default=0)
    stockcount = models.IntegerField(u'库存', default=0)
    copa = models.ForeignKey('Copa', u'合作社')
    gupdate = models.DateTimeField()

    def get_abstract(self, verbose):
        intro = {
            'id': self.id,
            'img': "{proto}://{domain}{path}".format(
                proto=config.PROTOCOL,
                domain=config.DOMAIN,
                path=self.img.url,
            ),
            'name': self.goodname,
            'price': self.goodprice,
            'copaname': self.copa.copaname,
            'copasec': self.copa.copasec,
        }
        if verbose == 'detial':
            intro['sec'] = self.gooddesc
            intro['salecount'] = self.salecount
            intro['stockcount'] = self.stockcount
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
