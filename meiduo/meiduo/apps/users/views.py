from django.shortcuts import render
from rest_framework.views import APIView
from .models import User, Address
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListCreateAPIView
from .serializers import CreateUserSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, SendEmailSerializer, AddressSerializer,HistorySerizlizer
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS
from django.conf import settings
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Address
from rest_framework.decorators import action

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
    def get(self, request):
        # 获取加密后的id
        token = request.query_params.get('token')
        de_salt = TJWSS(settings.SECRET_KEY, settings.EMAIL_EXPIRES)
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
        return Response({'message': 'OK'})


class AddressViewSet(ModelViewSet):
    # 要求登录 获取user
    permission_classes = [IsAuthenticated]
    # 查询的是地址表里的所有数据
    # queryset = Address.objects.filter(is_deleted=False)
    serializer_class = AddressSerializer
    # 用来给修改对象指定查询集
    queryset = Address.objects.filter(is_deleted=False)

    # queryset属性不能用了 则使用get_queryset方法
    # def get_queryset(self):
    #     # 获取当前登录的用户
    #     user = self.request.user
    #     return user.addresses.filter(is_deleted=False)

    # 由于不满足前端格式要求，所以重写get方法返回指定格式数据
    def list(self, request, *args, **kwargs):
        # 查询当前登录用户的所有收获地址
        user = self.request.user
        addresses = user.addresses.filter(is_deleted=False)

        serializer = self.get_serializer(addresses, many=True)

        return Response(
            {
                'addresses': serializer.data,
                'limit': 5,
                'default_address_id': user.default_address_id
            }
        )

    # 　需要更新地址继承UpdateModelMixin类,但需要配置一条新的路由
    # 不想配置多条路由，则可使用视图集,并重写list方法
    # 创建和更新操作该视图集自带了

    # 实现逻辑删除　重写方法
    def destroy(self, request, *args, **kwargs):
        # get_object 方法根据主键得到对象
        address = self.get_object()
        address.is_deleted = True
        # 保存更改
        address.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'],detail=True) # addresses/(pk)/status/
    def status(self,request,pk):
        # 设置默认收货地址
        user = request.user
        user.default_address_id = pk
        user.save()
        return Response({'message':'ok'})

    @action(methods=['put'],detail=True) # addresses/(pk)/title
    def title(self,request,pk):
        # 修改地址标题
        # 获取当前收货地址对象
        address = self.get_object()
        address.title = request.data.get('title')
        address.save()
        return Response({'message': 'ok'})


class SKUHistoryView(CreateAPIView):
    # 增加商品编号
    # 未登录用户不存储浏览记录
    permission_classes = [IsAuthenticated]
    serializer_class = HistorySerizlizer


