from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import SKU
from .serializers import SKUSerializer
from meiduo.utils.pagination import StandardResultsSetPagination
from rest_framework.filters import OrderingFilter
from drf_haystack.viewsets import HaystackViewSet
from .serializers import SKUIndexSerializer


class SKUList(ListAPIView):
    serializer_class = SKUSerializer
    # 希望得到某类商品的ＳＫＵ
    # 需要得到商品的分类id，所以只能使用方法来获得id
    def get_queryset(self):
        # 获取当前请求的参数，当前从请求路径中获取分类编号category_id
        id = self.kwargs.get('category_id')
        return SKU.objects.filter(category_id=id, is_launched=True)
    # 分页
    pagination_class = StandardResultsSetPagination
    # 排序
    filter_backends = (OrderingFilter,)
    ordering_fields = ('create_time', 'price', 'sales')

class SKUSearchViewSet(HaystackViewSet):
    """
    SKU搜索
    """
    index_models = [SKU]

    serializer_class = SKUIndexSerializer

    # 分页
    pagination_class = StandardResultsSetPagination