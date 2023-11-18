from django.db import models
from common.db import BaseModel
# django中自带的用户认证模型
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser, BaseModel):
    """"用户模型"""
    # id,username,password,email,is_active 继承于AbstractUser，所以不用写
    # created_time,updated_time 继承于BaseModel，所以不用写
    mobile = models.CharField(verbose_name='手机号', default='', max_length=11)
    avatar = models.ImageField(verbose_name='用户头像', blank=True, null=True)

    class Meta:
        db_table = 'users'
        verbose_name = '用户表'


class Addr(models.Model):
    """收货地址模型"""
    user = models.ForeignKey('User', verbose_name='所属用户', on_delete=models.CASCADE)  # 用户删除之后做一个级联删除
    phone = models.CharField(verbose_name='手机号码', max_length=11)
    name = models.CharField(verbose_name='联系人', max_length=20)
    province = models.CharField(verbose_name='省份', max_length=20)
    city = models.CharField(verbose_name='城市', max_length=20)
    county = models.CharField(verbose_name='区县', max_length=20)
    is_default = models.BooleanField(verbose_name='是否为默认地址', default=False)

    class Meta:
        db_table = 'addr'
        verbose_name = '收货地址表'


class Area(models.Model):
    """省市区县地址模型"""
    pid = models.ImageField(verbose_name='上级id')
    name = models.CharField(verbose_name='地区名', max_length=20)
    level = models.CharField(verbose_name='区域等级', max_length=20)

    class Meta:
        db_table = 'area'
        verbose_name = '地区表'


class VerifCode(models.Model):
    """验证码模型"""
    mobile = models.CharField(verbose_name='手机号',max_length=11)
    code = models.CharField(verbose_name='验证码', max_length=6)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='生成时间')

    class Meta:
        db_table = 'verifcode'
        verbose_name = '手机验证码表'

