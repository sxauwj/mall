from django.shortcuts import render
from rest_framework.views import APIView
from meiduo.utils.qq_sdk import OAuthQQ
from rest_framework.response import Response


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
        # https://graph.qq.com/oauth2.0/show?which=Login&display=pc&state=%2F&response_type=code&redirect_uri=http%3A%2F%2Fwww.meiduo.site%3A8080%2Foauth_callback.html&scope=get_user_info&client_id=101474184
        return Response({'login_url': url})
    # 浏览器回调地址并携带code
    #http://www.meiduo.site:8080/oauth_callback.html?code=BC9CACC4A6BED56042318CF64DC539E3&state=%2F

class QQUserView(APIView):
    def get(self,request):

        code = request.query