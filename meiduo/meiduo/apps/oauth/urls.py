from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^qq/authorization/$',views.OauthQQView.as_view())
]