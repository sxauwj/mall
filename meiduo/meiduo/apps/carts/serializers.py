from rest_framework import serializers
from goods.models import SKU


class CartSerializers(serializers.Serializer):
    sku_id = serializers.IntegerField()
    count = serializers.IntegerField(
        min_value=1,
        error_messages={
            'min_value':'至少添加一个'
        }
    )
    selected = serializers.BooleanField(default=True)

    def validate_sku_id(self,value):
        if SKU.objects.filter(pk=value).count() <= 0:
            raise serializers.ValidationError('商品编号无效')

        return value

