
from django.conf.urls import  url
from goods import views
#加载静态文件
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^register$', views.register),
    url(r'^index', views.index),
    url(r'^goods_view$', views.goods_view),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^login_action$', views.login_action),
    url(r'^user_info$', views.user_info),
    url(r'^update_address/(?P<address_id>\d+)$', views.update_address),
    url(r'^delete_address/(?P<address_id>\d+)$', views.delete_address),
    url(r'^add_address/(?P<sign>\d+)', views.add_address),
    url(r'^change_password$', views.change_password),
    url(r'^goods_view(?P<pindex>\d*)$', views.goods_view),
    url(r'^search_name$', views.search_name),
    url(r'^view_goods/(?P<good_id>\d+)$', views.view_goods),
    url(r'^add_chart/(?P<good_id>\d+)/(?P<sign>[0-9]+)$', views.add_chart),
    url(r'^view_chart$', views.view_chart),
    url(r'^remove_chart/(?P<good_id>\d+)$', views.remove_chart),
    url(r'^update_chart/(?P<good_id>\d+)', views.update_chart),
    url(r'^remove_chart_all$', views.remove_chart_all),
    url(r'^view_address$', views.view_address),
    url(r'^create_order', views.create_order),
    url(r'^view_order/(?P<orders_id>\d+)$',views.view_order),
    url(r'^view_all_chart$',views.view_all_chart),
    url(r'^delete_orders/(?P<orders_id>\d+)/(?P<sign>\d+)$',views.delete_orders),
]
