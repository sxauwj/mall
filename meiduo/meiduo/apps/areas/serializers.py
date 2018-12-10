from rest_framework import serializers
from .models import AreaInfo


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaInfo
        fields = ['id', 'name']


class SubSerializer(serializers.ModelSerializer):
    subs = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = AreaInfo
        fields = ['id', 'name', 'subs']
