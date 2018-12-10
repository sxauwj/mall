from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import AreaInfo
from .serializers import AreaSerializer, SubSerializer


class AreasViewSet(ReadOnlyModelViewSet):
    # list ==>查询列表
    # retrieve ==>查询单个对象

    # queryset = AreaInfo.objects.all()
    # serializer_class = AreaSerializer
    #　根据不同的请求提供不同的查询集
    def get_queryset(self):
        if self.action == 'list':
            return AreaInfo.objects.filter(parent=None)
        else:
            return AreaInfo.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AreaSerializer
        else:
            return SubSerializer






