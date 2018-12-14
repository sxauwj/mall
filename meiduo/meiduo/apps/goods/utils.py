from .models import GoodsChannel
def get_categories():
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
        channels = GoodsChannel.objects.order_by('group_id').order_by('sequence')

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

        return categories