from rest_framework import serializers
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS
from django.conf import settings
from . import constants
from users.models import User
from .models import OAuthQQUser
from meiduo.utils.jwt_token import generate_token


class QQSerializer(serializers.Serializer):
    # 负责接受校验的反序列化数据
    mobile = serializers.IntegerField(write_only=True)
    password = serializers.CharField(write_only=True)
    sms_code = serializers.IntegerField(write_only=True)
    # openid  write_only = True
    access_token = serializers.CharField(write_only=True)
    # 负责序列化输出的数据
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)

    def validated_mobile(self, value):
        pass

    def validated_sms_code(self, value):
        pass
        # def validated_password(self):
        #     pass

    def validate_access_token(self, value):
        tjwss = TJWSS(settings.SECRET_KEY, constants.OPENID_EXPIRES)
        try:
            json = tjwss.loads(value)
            print(json)
            print(json['openid'])
        except:
            raise serializers.ValidationError('授权信息超时')
        return json.get('openid')

    def create(self, validated_data):

        mobile = validated_data.get('mobile')
        password = validated_data.get('password')
        openid = validated_data.get('access_token')

        try:
            user = User.objects.get(mobile=mobile)
        except:
            user = User()
            user.mobile = mobile
            user.username = mobile
            user.set_password(password)
            user.save()
            qqauth = OAuthQQUser()
            qqauth.openid = openid
            qqauth.user = user
            qqauth.save()
            # 状态保持
            user.token = generate_token(user)

        else:
            # 检查密码是否正确
            if not user.check_password(password):
                raise serializers.ValidationError('用户名或密码错误')
            qqauth = OAuthQQUser()
            qqauth.openid = openid
            qqauth.user = user
            qqauth.save()
            user.token = generate_token(user)
        return user
