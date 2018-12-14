from .models import ContentCategory, Content
from goods import models
from django.shortcuts import render
from django.conf import settings
from goods.utils import get_categories
def generate_index_html():
    # 1.查询
    categories = get_categories()

    # 1.2查广告数据
    contents = {}
    content_categories = ContentCategory.objects.all()
    for content_category in content_categories:
        contents[content_category.key] = content_category.contents.filter(status=True).order_by('sequence')

        # 2生成html字符串
        context = {
            'categories':categories,
            'contents':contents
        }
        response = render(None,'index.html',context)
        # 获取html的响应体，且网络传输的数据是bytes的需要解码
        html_str = response.content.decode()

        # 3 写文件
        with open(settings.GENERATED_STATIC_HTML_FILES_DIR + 'index.html','w') as f:
            f.write(html_str)

