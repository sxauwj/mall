from meiduo.utils.meiduo_json import dumps, loads
from django_redis import get_redis_connection


def merge_cart_cookie_to_redis(request, user_id, response):
    # 获取cookie中的数据
    cookie_dict = request.COOKIES.get('cart')
    if not cookie_dict:
        return response
    cookie_dict = loads(cookie_dict)

    # 向redis中修改数据
    redis_cli = get_redis_connection('cart')
    p_c = redis_cli.pipeline()
    for sku_id, statu in cookie_dict.items():
        p_c.hset('cart_%d' % user_id, sku_id, statu.get('count'))
        if statu.get('selected'):
            p_c.sadd('cart_selected%d' % user_id, sku_id)
        else:
            p_c.srem('cart_selected%d' % user_id, sku_id)
    p_c.execute()
    # 通过response删除cookie中的数据
    response.delete_cookie('cart')

    # 响应
    return response
