from django.db import models


class BaseModel(models.Model):
    """抽象的模型基类：定义一些公共的模型字段"""
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        # 声明这是一个抽象的模型，在执行迁移文件时，不会在数据中生成表
        abstract = True
        verbose_name = '公共字段模型'
        db_table = 'BaseTable'
