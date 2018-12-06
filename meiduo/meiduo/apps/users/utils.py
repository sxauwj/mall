from django.contrib.auth.backends import ModelBackend
import re
from .models import User


class MeiduoModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # username可以是手机号，也可以是用户名
        if re.match(r'^1[3-9]\d{9}$', username):
            # 手机号
            try:
                user = User.objects.get(mobile=username)
            except:
                user = None
        else:
            # 用户名
            try:
                user = User.objects.get(username=username)
            except:
                user = None
        if user is not None:
            if not user.check_password(password):
                user = None
        # 返回
        return user
