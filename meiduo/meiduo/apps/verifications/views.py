from django.shortcuts import render

from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework.response import Response
import random
from . import constants


class SmsCode(APIView):
    def get(self, request, mobile):
        # 连接redis,指定cache中的键
        redis_cli = get_redis_connection('sms_code')
        # 验证是否发过短信
        if redis_cli.get('sms_flag_' + mobile):
            return Response({'message': '已经发送'})
        # 若未发过则生成六位随机验证码
        sms_code = random.randint(100000, 999999)
        # 将随机数保存到redis
        # 将发送标记保存到redis
        # 只与redis交互一次存入两个数据,redis的管道pipline,使操作具有原子性和减少客户端与服务端的连接开销
        redis_pipeline = redis_cli.pipeline()
        redis_pipeline.setex('sms_code_' + mobile, constants.SMS_CODE_EXPIRES, sms_code)
        redis_pipeline.setex('sms_flag_' + mobile, constants.SMS_FLAG_EXPIRES, 1)
        redis_pipeline.execute()
        # 调用第三方发送验证码
        print(sms_code)
        # 响应
        return Response({'message': 'ok'})
