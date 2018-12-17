from django.shortcuts import render
from rest_framework.views import APIView
from meiduo.utils.qq_sdk import OAuthQQ
from rest_framework.response import Response
from .models import OAuthQQUser
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS
from . import constants
from django.conf import settings
from meiduo.utils import jwt_token
from rest_framework.generics import CreateAPIView
from .serializers import QQSerializer
from carts.utils import merge_cart_cookie_to_redis

class OauthQQView(APIView):
    def get(self, request):
        """
        生成授权的url地址
        :param request:
        :return:
        """
        log = OAuthQQ()
        url = log.get_qq_login_url()
        # ur地址为：
        # https://graph.qq.com/oauth2.0/show?which=Login&display=pc&state=%2F&response_type=code&redirect_uri=http%3A%2F          %2Fwww.meiduo.site%3A8080%2Foauth_callback.html&scope=get_user_info&client_id=101474184
        return Response({'login_url': url})
        # 浏览器回调地址并携带code

        # http://www.meiduo.site:8080/oauth_callback.html?code=BC9CACC4A6BED56042318CF64DC539E3&state=%2F
        # 回调网址执行js　执行下面的视图


class QQAuthUserView(CreateAPIView):
    def get(self, request):
        # 　获得code
        code = request.query_params.get('code')

        # 请求资源
        auth = OAuthQQ()
        # 获得token
        token = auth.get_access_token(code=code)
        # 获得openid
        openid = auth.get_openid(token)

        # 将Q　和网站帐号绑定
        try:
            # 使用openid进行查询
            qq_loginer = OAuthQQUser.objects.get(openid=openid)
        except:
            # 查询不到则返回加密的openid,并提示绑定
            tjwss = TJWSS(settings.SECRET_KEY, constants.OPENID_EXPIRES)
            json = {'openid': openid}
            data = tjwss.dumps(json)
            return Response({'access_token': data})
        else:
            # 查询到则进行状态保持，token,user_id,username
            token = jwt_token.generate_token(qq_loginer.user)
            print(qq_loginer.user)
            data = {
                'user_id': qq_loginer.user.id,
                'username': qq_loginer.user.username,
                'token': token
            }
            response = Response(data)
            # 已经授权再次登录直接合并购物车
            response = merge_cart_cookie_to_redis(request,qq_loginer.user.id,response)
            return response

    # 凡是没有帐号的则创建帐号
    serializer_class = QQSerializer

    # 合并购物车,在序列化器中无法得到response所以在视图中重写post方法
    def post(self,request):
        response = super().post(request)

        if 'user_id' in response.data:
            user_id = response.data.get('user_id')

        response = merge_cart_cookie_to_redis(request,user_id,response)

        return response





