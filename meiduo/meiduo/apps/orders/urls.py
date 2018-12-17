from django.conf.urls import url
from . import views

urlpatterns = [
    url('^settlement/$',views.SettlementView.as_view()),
    url('^$',views.OrderView.as_view()),
]