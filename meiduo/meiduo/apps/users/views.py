from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from .serializers import CreateUserSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer


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
