from rest_framework import serializers
from .models import User
import re
from django_redis import get_redis_connection
# 手动签发ＪＷＴ
from rest_framework_jwt.settings import api_settings

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
    token = serializers.CharField(label='登录状态token',read_only=True)
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
        fields = ['id','username','mobile','email','email_active']
