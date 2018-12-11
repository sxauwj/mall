from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import AreaInfo
from .serializers import AreaSerializer, SubSerializer
#CacheResponseMixin为视图集同时补充List和Retrie两种缓存，与ListModelMixin和RetrieveModelMixin一起配合使用
from rest_framework_extensions.cache.mixins import CacheResponseMixin


class AreasViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    # list ==>查询列表
    # retrieve ==>查询单个对象

    # queryset = AreaInfo.objects.all()
    # serializer_class = AreaSerializer
    #　根据不同的请求提供不同的查询集
    def get_queryset(self):
        if self.action == 'list':
            # 查询列表时返回省的列表
            # areas/
            return AreaInfo.objects.filter(parent=None)
        else:
            # 查询某个对象时
            # retrive
            # areas/pk
            return AreaInfo.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AreaSerializer
        else:
            return SubSerializer






