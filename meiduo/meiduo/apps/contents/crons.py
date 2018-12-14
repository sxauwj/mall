from .models import ContentCategory, Content
from goods import models
from django.shortcuts import render
from django.conf import settings

def generate_index_html():
    # 1.查询
    # categories = {
    #     1: { # 组1
    #         'channels': [{'id':, 'name':, 'url':},{}, {}...],
    #         'sub_cats': [{'id':, 'name':, 'sub_cats':[{},{}]}, {}, {}, ..]
    #     },
    #     2: { # 组2
    #
    #     }
    # }
    # 1.1查询分类数据
    channels = models.GoodsChannel.objects.order_by('group_id').order_by('sequence')

    categories = {}
    for channel in channels:
        if channel.group_id not in categories:
            categories[channel.group_id] = {
                'channels': [],
                'sub_cats': []
            }
        # 频道已经添加到频道字典中了，添加一级分类
        categories[channel.group_id]['channels'].append({
            'id': channel.category_id,
            'name': channel.category.name,
            'url': channel.url
        })

        # sub_cats2 = []
        # 遍历二级分类
        for sub_cat2 in channel.category.subs.all():

            # 遍历三级分类
            sub_cats3 = []
            for sub_cat3 in sub_cat2.subs.all():
                sub_cats3.append(sub_cat3)
            # 添加三级分类
            sub_cat2.sub_cats = sub_cats3

        # 向频道中添加二级分类
            categories[channel.group_id]['sub_cats'].append(sub_cat2)

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

