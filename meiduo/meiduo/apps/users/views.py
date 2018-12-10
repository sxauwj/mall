from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from .serializers import CreateUserSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, SendEmailSerializer
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS
from django.conf import settings
from rest_framework import status

class UsernameCountView(APIView):
    """用户名数量"""

    def get(self, requeset, username):
        count = User.objects.filter(username=username).count()
        data = {
            'username': username,
            'count': count
        }
        return Response(data)


class MobileCountView(APIView):
    """手机号数量"""

    def get(self, request, mobile):
        print('检验')
        count = User.objects.filter(mobile=mobile).count()
        data = {
            'mobile': mobile,
            'count': count
        }
        print(data)
        return Response(data)


class UserView(CreateAPIView):
    serializer_class = CreateUserSerializer


class UserInfoView(RetrieveAPIView):
    # 要求登录后才能访问
    permission_classes = [IsAuthenticated]

    # 个人信息显示页面，显示的数据需要获取当前登录的用户而不是主键
    def get_object(self):
        print(self)
        """
        获取对象，用于retrive,destroy,update
        :return:
        """
        # 默认实现是获取pk,查询对象
        # 不想使用默认方法,重写该方法，如获取当前登录的用户
        return self.request.user

    serializer_class = UserSerializer
    pass


class SendEmailView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    # 重写get_object()方法，获取当前登录的用户
    def get_object(self):
        user = self.request.user
        return user

    serializer_class = SendEmailSerializer

class EmailActiveView(APIView):
    def get(self,request):
        # 获取加密后的id
        token = request.query_params.get('token')
        de_salt = TJWSS(settings.SECRET_KEY,settings.EMAIL_EXPIRES)
        try:
            id_dict = de_salt.loads(token)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_id = id_dict.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.email_active = True
        user.save()
        return Response({'message':'OK'})







