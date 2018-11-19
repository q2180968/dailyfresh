from django.db import models
from tinymce.models import HTMLField


# Create your models here.
# 商品类目模型
class TypeInfo(models.Model):
    tname = models.CharField(max_length=32)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.tname

    class Meta():
        db_table = 'typeinfo'


# 商品模型
class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=32)
    gpic = models.ImageField(upload_to='df_goods')
    gprice = models.DecimalField(max_digits=10, decimal_places=2)
    gunit = models.CharField(max_length=20, default='500g')
    gclick = models.IntegerField(default=0)
    gjianjie = models.CharField(max_length=200)
    gkuncun = models.IntegerField()
    gcontent = HTMLField()
    gacv = models.BooleanField(default=False)
    isDelete = models.BooleanField(default=False)

    gtype = models.ForeignKey(TypeInfo, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.gtitle

    class Meta():
        db_table = 'goodsinfo'
