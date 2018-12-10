from celery_tasks.main import app
from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS
from django.conf import settings


@app.task(name='send_email')
def send_email(to_email, user_id):

    # 定义方法，封装耗时代码
    # 将用户id加密，再放到链接地址中
    add_salt = TJWSS(settings.SECRET_KEY,settings.EMAIL_EXPIRES)
    dict = {'user_id':user_id}
    token = add_salt.dumps(dict).decode()

    hl_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="http://www.meiduo.site:8080/success_verify_email.html?token=%s">点击激活<a></p>' % (to_email, token)

    send_mail('美多商城－激活邮件',
              '',
              settings.EMAIL_FROM,
              [to_email],
              html_message=hl_message
              )
