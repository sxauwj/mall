from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .serializers import CreateUserSerializer
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


