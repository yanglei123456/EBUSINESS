from goods.object import Orders_list,Order_list
from goods.models import Goods
from goods.object import Chart_list

class Util():

#该程序是为了通过ccookie 和session 获取用户名和密码;
    def get_name(self,request):
      
        username = request.session.get('username','')
        cookie_list =request.COOKIES
# cookie_list =  {'csrftoken': 'UjjmGHaAEKVdCRFnOhdjmASXffhEOzpu', 'sessionid': 'zud33aqjhmnm6ab9itx9on0ioyrfj5q2', '8': '1', '11': '1', '9': '1', '7': '1', '6': '1'}
        if ('sessionid' in cookie_list) and (username is not None):
            return username
        else:
            return ''

#通过cookir返回购物车的商品数目
    def cookies_count(self,request):
        cookie_list = request.COOKIES
        if "crsftoken" in cookie_list:
            return len(cookie_list)-2
        else:
            return len(cookie_list)-1
#获取cookie_list 中的购物车cookie 
    def deal_cookies(self,request):
        cookie_list = request.COOKIES
        cookie_list.pop('sessionid')
        if 'csrftoken' in cookie_list:
            cookie_list.pop('csrftoken')
        return cookie_list          

#将上一步得到的cookie_list 加入到购物车中
    def add_chart(self,request):
        cookie_list = self.deal_cookies(request)
        my_chart_list = []
        for key in cookie_list:
           # chart_object = Chart_list()
           #原书中有上面 我认为有问题没写
            chart_object = self.set_chart_list(key,cookie_list)
            my_chart_list.append(chart_object)
        print('$$$$$$$$$$$$$$$$$$$')
        print (my_chart_list)
        return my_chart_list
    
    def set_chart_list(self,key,cookie_list):
        chart_list = Chart_list()
        good = Goods.objects.get(id=key)
        chart_list.set_id(key)
        chart_list.set_name(good.name)
        chart_list.set_price(good.price)
        chart_list.set_count(cookie_list[key])
        return chart_list

#定义订单变量 key 为order数据库中的每一个order,将每一个order实例化，并给属性
    def set_order_list(self,key):
        order_object=Order_list()
        order_object.set_id(key.id)
        good_list = Goods.objects.get(id = key.goods_id)
        order_object.set_good_id(good_list.id)
        order_object.set_name(good_list.name)
        order_object.set_price(good_list.price)
        order_object.set_count(key.count)
        return order_object

#查看所有订单，key为orders 数据库中每一个orders
    def set_orders_list(self,key):
        orders_object=Orders_list()
        orders_object.set_id(key.id) 
        orders_object.set_address(key.address)
#上一步 不确定如何根据外键获取外间关联的其他表的属性
        orders_object.set_create_time(key.create_time)
        return orders_object
