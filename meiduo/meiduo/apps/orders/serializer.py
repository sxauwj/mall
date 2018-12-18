from rest_framework import serializers
from .models import OrderInfo, OrderGoods
from goods.models import SKU

from datetime import datetime
from django_redis import get_redis_connection
from django.db import transaction

class OrderSerializer(serializers.Serializer):
    address = serializers.IntegerField(write_only=True)
    pay_method = serializers.IntegerField(write_only=True)
    order_id = serializers.CharField(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user

        # 1.创建OrderInfo对象
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + '%09d' % user.id
        if validated_data.get('pay_method') == 2:
            # 待支付
            status = 1
        else:
            status = 2
        total_count = 0
        total_amount = 0

        # 开启事务
        with transaction.atomic():
            # 创建保存点
            save_id = transaction.savepoint()

            order = OrderInfo.objects.create(
                order_id=order_id,
                user_id=user.id,
                address_id=validated_data.get('address'),
                total_count=total_count,
                total_amount=total_amount,
                pay_method=validated_data.get('pay_method'),
                status=status,
                freight=10
            )
            # 读取redis中选中的商品
            redis_cli = get_redis_connection('cart')

            cart_dict = redis_cli.hgetall('cart_%d' % user.id)

            cart_selected = redis_cli.smembers('cart_selected%d' % user.id)

            cart_dict = {int(sku_id): int(count) for sku_id, count in cart_dict.items()}

            cart_selected = [int(sku_id) for sku_id in cart_selected]

            cart_sku = SKU.objects.filter(pk__in=cart_selected)
            # ４遍历商品对象列
            for sku in cart_sku:

                count = cart_dict[sku.id]
                # 4.1 判断库存，如果库存不足，则抛异常
                if sku.stock < count:
                    transaction.savepoint_rollback(save_id)
                    raise serializers.ValidationError('库存不足')
                sku.stock -= count
                sku.sales += count
                sku.save()

                # 创建OrderGoods对象
                order_goods = OrderGoods.objects.create(
                    order_id = order_id,
                    sku_id=sku.id,
                    price=sku.price,
                    count=count,
                )

                # 4.4计算总数量，总金额
                total_count += count
                total_amount += count * sku.price

            # 修改订单的总数量，总金额
            order.total_count = total_count
            order.total_amount = total_amount
            order.save()
            transaction.savepoint_commit(save_id)

        # 删除redis中的商品信息
        redis_cli.srem('cart_selected%d' % user.id, *cart_selected)
        redis_cli.hdel('cart%d' % user.id, *cart_selected)

        return order
