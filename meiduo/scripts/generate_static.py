#!/usr/bin/env python
# /usr/bin/env 表示查找指定命令的路径，如查找python的路径，会在当前服务器磁盘上查找
# /home/python/.virtualenvs/django_py3/bin/python ==>路径固定了不灵活
#指定python解释器


import sys
import os
import django

# 指定python解释器的导包路径，当前指定为manage.py同级目录
# sys.path.insert(0, '../')

# 读取配置，设置环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo.settings.dev")

# django初始化
django.setup()

from goods.models import SKU
from celery_tasks.generic_detail.tasks import generate_static_sku_detail_html

if __name__ == '__main__':
    skus = SKU.objects.all()
    for sku in skus:
        generate_static_sku_detail_html(sku.id)
    print('ok')
