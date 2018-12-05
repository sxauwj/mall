from celery import Celery

# 为celery使用django配置文件进行设置，任务可能会用到配置
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo.settings.dev'

# 创建celery应用
app = Celery('meiduo')

# 导入celery配置
app.config_from_object('celery_tasks.config')

# 自动注册celery任务
app.autodiscover_tasks([
    'celery_tasks.sms_code'
])