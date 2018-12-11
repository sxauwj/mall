from django.conf.urls import url
from . import views
# DRF JWK提供了登录签发JWT的视图，可以直接使用
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    url(r'^users/$', views.UserView.as_view()),
    url(r'^authorizations/$', obtain_jwt_token),
    url(r'^user/$',views.UserInfoView.as_view()),
    url(r'^emails/$',views.SendEmailView.as_view()),
    url(r'^emails/verification/$',views.EmailActiveView.as_view()),
    # url('^addresses/$',views.AddressViewSet.as_view()),
]

router = DefaultRouter()
router.register('addresses',views.AddressViewSet,base_name='addresses')
urlpatterns += router.urls
