# coding:utf-8

from django.db import models
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


class ApiTest(models.Model):
    jk_id = models.IntegerField(verbose_name='健客ID')
    taobao_id = models.IntegerField(verbose_name='淘宝ID')
    prod_name = models.CharField(verbose_name='商品名', max_length=300)
    prod_class = models.CharField(verbose_name='类别', max_length=100)
    num = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    marigin = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    real_name = models.CharField(max_length=255)
    shop_name = models.CharField(max_length=255)
    price_rank = models.IntegerField()
    price_idx = models.CharField(max_length=20)
    owner = models.ForeignKey('auth.User', related_name='apitest', on_delete=models.CASCADE, null=True)
    highlighted = models.TextField(null=True)

    #def save(self, *args, **kwargs):
    #    """
    #    Use the `pygments` library to create a highlighted HTML
    #    representation of the code snippet.
    #    """
    #    price = self.price and 'table' or False
    #    options = self.taobao_id and {'taobao_id': self.taobao_id} or {}
    #    formatter = HtmlFormatter(jk_id=self.jk_id, price=price,
    #                              full=True, **options)
    #    self.highlighted = highlight(self.num, formatter)
    #    super(ApiTest, self).save(*args, **kwargs)

    class Meta:
        db_table = 'api_test'



