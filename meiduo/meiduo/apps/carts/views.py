from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CartSerializers, CartListSerializer
from meiduo.utils.meiduo_json import dumps, loads
from .constants import COOKIE_EXPIRES
from goods.models import SKU


class CartView(APIView):
    def perform_authentication(self, request):
        '''
        在视图方法执行前，不再进行身份认证
        :param request:
        :return:
        '''
        pass

    def post(self, request):
        # 接受数据
        data = request.data
        # 验证：使用序列化器
        serializer = CartSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        sku_id = serializer.validated_data.get('sku_id')
        count = serializer.validated_data.get('count')
        selected = serializer.validated_data.get('selected')

        # 获取cookie
        cart_cookie_dict = request.COOKIES.get('cart')
        print('拿到的cookie', cart_cookie_dict)
        # 第一次添加购物车，未获取到cookie则准备cart_cookie字典
        if not cart_cookie_dict:
            cart_cookie_dict = {}
        else:
            # 获取到cookie解码成字典
            cart_cookie_dict = loads(cart_cookie_dict)

        # 将物品添加到cookie中
        print(sku_id, count)
        print(cart_cookie_dict)

        cart_cookie_dict[sku_id] = {
            'count': count,
            'selected': selected,
        }

        # 创建响应对象
        response = Response(serializer.validated_data)
        # 将cookie转成字符串
        cart_cookie_str = dumps(cart_cookie_dict)
        # 添加cookie
        response.set_cookie('cart', cart_cookie_str, max_age=COOKIE_EXPIRES)

        # 响应
        return response

    def get(self, request):
        cart_dict = request.COOKIES.get('cart')
        if not cart_dict:
            return Response({'message': 'no data'})
        # 将cookie解码成字典
        cart_dict = loads(cart_dict)
        # 遍历字典
        # 接受sku对象集合
        skus = []
        for sku_id, sku_statu in cart_dict.items():
            try:
                sku = SKU.objects.get(pk=sku_id)
            except:
                pass
            else:
                sku.selected = sku_statu['selected']
                sku.count = sku_statu['count']
                skus.append(sku)
        # 序列化输出sku对象　
        serializer = CartListSerializer(skus, many=True)
        return Response(serializer.data)

    def put(self, request):
        # 接受请求体中的参数
        cart_dict = request.data

        # 验证
        serializer = CartSerializers(data=cart_dict)
        serializer.is_valid(raise_exception=True)
        sku_id = serializer.validated_data['sku_id']
        count = serializer.validated_data['count']
        selected = serializer.validated_data['selected']
        # 读取cookie中的数据
        cart_dict = request.COOKIES.get('cart')
        if cart_dict is None:
            return Response({'message': 'no data'})

        cart_dict = loads(cart_dict)

        if sku_id not in cart_dict:
            return Response({'message': 'no data'})

        # 修改cookie中的数据
        cart_dict[sku_id]['count'] = count
        cart_dict[sku_id]['selected'] = selected

        # 创建响应对象
        response = Response()

        # 设置cookie
        response.set_cookie('cart', dumps(cart_dict), COOKIE_EXPIRES)
        # 返回响应
        return response
