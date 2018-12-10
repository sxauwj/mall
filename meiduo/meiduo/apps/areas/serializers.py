from rest_framework import serializers
from .models import AreaInfo


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaInfo
        fields = ['id','name']

class SubSerializer(serializers.ModelSerializer):
    subs = AreaSerializer()
    class Meta:
        model = AreaInfo
        fields = ['id','name','subs']


