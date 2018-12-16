from rest_framework import serializers
from .models import User
import re
from django_redis import get_redis_connection
# 手动签发ＪＷＴ
from rest_framework_jwt.settings import api_settings
from celery_tasks.send_email.tasks import send_email
from .models import Address
from goods.models import SKU


class CreateUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        min_length=5, max_length=20,
        error_messages={
            'min_length': '用户名位5-20个字符',
            'max_length': '用户名位5-20个字符'
        }
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=20,
        error_messages={
            'min_length': '密码为8-20个字符',
            'max_length': '密码为8-20个字符'
        }
    )
    password2 = serializers.CharField(write_only=True)
    sms_code = serializers.IntegerField(write_only=True)
    mobile = serializers.CharField()
    allow = serializers.CharField(write_only=True)
    # token字段
    token = serializers.CharField(label='登录状态token', read_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).count() > 0:
            raise serializers.ValidationError('用户名存在')
        return value

    def validated_mobile(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')
        return value

    def validate_allow(self, value):
        if not value:
            raise serializers.ValidationError('请勾选协议')

    def validate(self, attrs):
        print('用户名为:', attrs.get('username'))
        # 短信验证码
        # 连接redis数据库
        redis_cli = get_redis_connection('sms_code')
        key = 'sms_code_' + attrs.get('mobile')
        sms_code_redis = redis_cli.get(key)
        if not sms_code_redis:
            raise serializers.ValidationError('验证码已经过期')
        redis_cli.delete(key)
        sms_code_redis = sms_code_redis.decode()
        print(sms_code_redis)
        print(type(sms_code_redis))
        sms_code_request = attrs.get('sms_code')
        if int(sms_code_redis) != sms_code_request:
            raise serializers.ValidationError('验证码错误!')

        # 验证两个密码是否相等
        pwd1 = attrs.get('password')
        pwd2 = attrs.get('password2')
        if pwd1 != pwd2:
            raise serializers.ValidationError('两次输入的密码不相同')

        return attrs

    def create(self, validated_data):

        print(validated_data.get('username'))
        user = User()
        user.username = validated_data.get('username')
        user.mobile = validated_data.get('mobile')
        user.set_password(validated_data.get('password'))
        user.save()

        # 注册成功，状态保持，生成jwt
        # 1.获取生成payload方法
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 2.获取生成token的方法（获取编码方法）
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # 3.根据用户对象生成载荷
        payload = jwt_payload_handler(user)
        # 4.根据载荷生成token
        token = jwt_encode_handler(payload)
        # 5.输出
        user.token = token
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'email', 'email_active']


class SendEmailSerializer(serializers.ModelSerializer):
    """
    邮箱序列化器
    """

    class Meta:
        model = User
        fields = ['id', 'email']

    def update(self, instance, validated_data):
        # 设置用户的邮箱
        # instance.email = validated_data['email']
        # instance.save()
        # 重写update方法，保持原有的操作不变，新增发邮件
        result = super().update(instance, validated_data)

        # 调用进程发送邮件
        send_email.delay(validated_data.get('email'), instance.id)
        return result


class AddressSerializer(serializers.ModelSerializer):
    # 隐含属性需要专门指定，省市区的外键，通过_id进行设置
    province_id = serializers.IntegerField()
    city_id = serializers.IntegerField()
    district_id = serializers.IntegerField()
    # 省市区的信息，以字符串的形式输出,输出关联属性，默认输出主键
    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Address
        exclude = ['title','is_deleted','user']

    # 验证信息省略

    def create(self, validated_data):
        # 接受数据，为属性赋值，创建
        # 重写此方法，添加user_id参数，不接受客户端传递的user_id参数
        # 创建对象并返回
        validated_data['user_id'] = self.context['request'].user.id
        validated_data['title'] = validated_data['receiver']
        return super().create(validated_data)

class HistorySerizlizer(serializers.Serializer):
    sku_id = serializers.IntegerField()

    def validate_sku_id(self,value):
        sku = SKU.objects.filter(pk=value)
        if not sku :
            raise serializers.ValidationError('无商品信息')
        return value

    def create(self,validated_data):
        """
        向redis的指定的库，添加指定商品的编号
        :param validated_data:
        :return:
        """
        sku_id = validated_data['sku_id']
        # 连接redis
        user  = self.context['request'].user
        redis_cli = get_redis_connection('history')
        key = 'history%d' % user.id

        # 删除键
        redis_cli.lrem(key,0,sku_id)

        # 添加键
        redis_cli.lpush(key,sku_id)

        # 截取
        redis_cli.ltrim(key,0,4)

        return validated_data








