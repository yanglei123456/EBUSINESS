from django.shortcuts import render,redirect
from goods.models import User,Order,Orders,Address,Goods
# Create your views here.
from django.db import models
from goods.form import UserForm,LoginForm,AddressForm
#from django.http import HttpResponse
from goods.util import Util
#定义一个通过session和cookie获取名字的函数,封装到util.py中
#def get_name(request):
 #   username = request.session.get('username','')
  ## if ('sessionid' in cookie_list) and (username is not None):
    #    return username
    #else:
     #   return ''
#自己定义登录装饰器
def login_decorate(view_func):
    def wrapper(request,*args,**kwargs):
        util = Util()
        username = util.get_name(request)
        if username =='':
            uf = LoginForm()
            return render(request,'goods/index.html',{'uf':uf,'error':'请登录后再操作'})
        else:
            return view_func(request,util,username,*args,**kwargs)
    return wrapper
#注册
def register(request):
    if request.method !='POST':
        uf = UserForm()
        return render(request,'goods/register.html',{'uf':uf}) 

    else:
       # return HttpResponse('ok')
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = (request.POST.get('username')).strip()
            password = (request.POST.get('password')).strip()
            email = (request.POST.get('email')).strip()
#核对是否有同名的
            user_list = User.objects.filter(username=username)
            if user_list:
                return render(request,'goods/register.html',{'uf':uf,'error':'该用户名已存在'})
            else:
            #此时注册成功
                user = User()
                user.username=username
                user.password=password
                user.email=email
                user.save()
                uf = LoginForm()
                return render(request,'goods/index.html',{'uf':uf})
                #return redirect('/index.html')
def index(request):
    uf = LoginForm()
    return render(request,'goods/index.html',{'uf':uf})
def login(request):
    uf = LoginForm()
    return render(request,'goods/index.html',{'uf':uf})
def logout(request):
    request.session['username']=''
    uf = LoginForm()
    return render(request,'goods/index.html',{'uf':uf})

def login_action(request):
    if request.method =='POST':
        uf = LoginForm(request.POST)
        if uf.is_valid:
            user_name = (request.POST.get('username','')).strip()
            pass_word = (request.POST.get('password','')).strip()
            if user_name =='' or pass_word =='':
                return render(request,'index.html',{'uf':uf,'error':'姓名和密码不能为空'})
            else:
                #核对姓名和密码信息是否正确
                obj = User.objects.filter(username=user_name,password=pass_word)
                if obj :
                    response = redirect('/goods_view')
                    request.session['username']=user_name
                    return response
                else:
                    return render(request,'goods/index.html',{'uf':uf,'error':'姓名和密码不正确，请重新输入'})



def goods_view(request):
    return render(request,'goods/goods_view.html')
 

#定义个人中心，显示个人信息
def user_info(request):
    util = Util()
    username = util.get_name(request)
    if username =='':
        return redirect('/index.html')
    else:
        user_list = User.objects.get(username=username)
        print('++++++++++++++')
        
       # user_address = Address.objects.get(user_id = user_list.id)
#user_address = Address.objects.filter(user_id = user_list.id)
        address_list = Address.objects.filter(user_id = user_list.id)
        print('~~~~~~~~~~~~~~~~~')
        #print(user_address)
        print('-----------------')
       #当用filter代替get 后 user_address.pthone无输出
        #password=user_list.password
       # print (user_address.phone)
        #return render(request,'goods/user_info.html',{'user_list':user_list,'username':username,'useraddress':user_address})
        return render(request,'goods/user_info.html',{'user_list':user_list,'username':username,'useraddress':address_list})
#修改地址
@login_decorate
def update_address(request,util,username,address_id):
    user_list = Address.objects.get(id = address_id)
    if request.method != 'POST':
        print('_________method________')
        return render(request,'goods/update_address.html',{'user_list':user_list,'address_id':address_id})
    else:
        uf = AddressForm(request.POST)
        new_address = (request.POST.get('new_address','')).strip()
        new_phone = (request.POST.get('new_phone','')).strip()
        print(new_address)
        print(new_phone)
        check = Address.objects.filter(address=new_address,user_id=user_list.id)
        if not check:
            Address.objects.filter(id=address_id).update(address=new_address)
            Address.objects.filter(id=address_id).update(phone=new_phone) 
        else:
            return render(request,'goods/update_address.html',{"error":'该地址已经存在，请重新输入'})
        address_list=Address.objects.filter(user_id =user_list.id)
        return redirect('/user_info')
        #return render(request,'goods/user_info.html',{'user_list':user_list,'username':username,'useraddress':address_list})
    #pass

#删除地址
@login_decorate
def delete_address(request,util,username,address_id):
    user_list = User.objects.get(username = username)
    Address.objects.filter(id = address_id).delete()
    address_list =Address.objects.filter(user_id=user_list.id)
    return redirect('/user_info')

#添加地址 可以在个人中心添加地址 可以在 提交订单的时候添加地址，这样对应返回不一样的页面，引入sign参数1/2
@login_decorate
def add_address(request,util,username,sign):
    user_list = User.objects.get(username = username)
    id = user_list.id
    print(sign)
    if request.method !='POST':
        uf = AddressForm()
        return render(request,'goods/add_address.html',{'uf':uf})
    else:
        uf = AddressForm(request.POST)
        if uf.is_valid():
            new_address = (request.POST.get('address','')).strip()
            new_phone = (request.POST.get('phone','')).strip()
            #判断地址是否已经存在
            check = Address.objects.filter(address = new_address,user_id = id )
            if check:
                return render(request,'goods/add_address.html',{'error':'该地值已经存在'})
            else:
                address = Address()
                address.user_id = id
                address.phone = new_phone
                address.address = new_address
                address.save()
                if sign == '1':
                    return redirect('/user_info')
                else:
                    address_list = Address.objects.filter(user_id = id)
#return render(request,'goods/view_address.html',{''})
                    return HttpResponse('ok')
#更改密码
def change_password(request):
    util = Util()
    username = util.get_name(request)
    if username =='':
        return redirect('/index.html')
    else:
        if request.method =='POST':
            #1如果旧密码不正确
            password = (User.objects.get(username=username)).password
            oldpassword = (request.POST.get('oldpassword','')).strip()
            password1 = (request.POST.get('password1','')).strip()
            password2 = (request.POST.get('password2','')).strip()
           #print("___________________________")
            print(password1)
            #print("*************************")
            print(password2)
            if password != oldpassword:
                msg = '旧密码输入错误，请重输'
                return render(request,'goods/change_password.html',{'error':msg}) 
            #2如果两次新密码不一样
            elif password1 != password2:
                msg = '两次新密码不一样，请重输'
                return render(request,'goods/change_password.html',{'error':msg}) 

            elif password1 == password2 and(password2==''):
                msg = '请重新输入非空新密码'
                return render(request,'goods/change_password.html',{'error':msg}) 
            #3如果旧密码正确 两个新密码一样
            elif password2==password1:
                User.objects.filter(username = username).update(password=password1)
                return HttpResponse('修改密码成功')

        else:
            return render(request,'goods/change_password.html')

from django.core.paginator import Paginator
def goods_view(request,pindex=1):
    util = Util()
    username = util.get_name(request)
    goodss = Goods.objects.all()
    #翻页操作
    paginator = Paginator(goodss,4)
    if pindex =='':
        pindex =1
    else:
        pindex = int(pindex)
    page = paginator.page(pindex)

    return render(request,'goods/goods_view.html',{'page':page})


#商品搜索
def search_name(request,pindex=1):
    if request.method !='POST':
        return render(request,'goods/search_name.html')
    else:
        '''util = Util()
        username = util.get_name(request)
        print(username)
         if username =='':
       # uf = LoginForm()
        #print('________'）
        return render(request,"goods/index.html",{"error":"请登录后再进入"})
#return redirect('/index.html')
    # return render(request,'goods/index.html',{'uf':uf,'error':'请登录后再操作'})
    else:
        print(username)'''
        print('------------')
        s_name = request.POST.get('s_name')
        print(s_name)
        print("++_______++++")
        goods_list = Goods.objects.filter(name=s_name)
        #get 得到的不可迭代
        print(goods_list)
        
        #对内容分页显示
        paginator = Paginator(goods_list,3)
        pindex=int(pindex)
        page = paginator.page(pindex)
        print('++++++++++')
        return render(request,'goods/goods_view.html',{'page':page})
#商品详情页
#该详情页有问题，不能够呈现出来商品的picture
def view_goods(request,good_id):
    content = Goods.objects.get(id = good_id)
    print("+++++++++++++")
    print(content.picture)
    return render(request,'goods/view_goods.html',{'content':content})

#购物车
#将商品放入购物车ad/goods.id/1huo2 仅设置cookie网页不发生变化
def add_chart(request,good_id,sign):
    util =Util()
    username = util.get_name(request)
    if username =='':
        return redirect('/index.html')
    else:
        #get_object_or_404的介绍： 我们原来调用django 的get方法，如果查询的对象不存在的话，会抛出一个DoesNotExist的异常， 现在我们调用django get_object_or_404方法，它会默认的调用django 的get方法， 如果查询的对象不存在的话，会抛出一个Http404的异常，我感觉这样对用户比较友好， 如果用户查询某个产品不存在的话，我们就显示404的页面给用户，比直接显示异常好
        #good = get_object_or_404(Goods,id = good_id)
        good = Goods.objects.get(id = good_id)
        if sign == '1':
            response = redirect('/goods_view')
        else:
            print("[[][][][][]][]]")
            response = redirect('/view_goods/'+good_id)
            print('1133311')
        response.set_cookie(str(good_id),1,60*60*24*180)
      #  print(request.COOKIES[str(good_id)])
        print(request.COOKIES)
        print("-----------------")
        return response


#查看购物车
@login_decorate
def view_chart(request,util,username):
   # util =Util()
 #   username = util.get_name(request)
  #  if username =='':
  #      uf = LoginForm()
        #return redirect('/index.html')
 #       return render(request,'goods/index.html',{'uf':uf,'error':'请登录后再操作'})
   # else:
        #购物车中的商品数
    count = util.cookies_count(request)
    my_chart_list = util.add_chart(request)       
    print("******************")
    print(my_chart_list)
    return render(request,'goods/view_chart.html',{'username':username,'goods':my_chart_list})
#删除购物车的某个商品
@login_decorate        
def remove_chart(request,util,username,good_id):
    response = redirect('/view_chart')
    response.set_cookie(str(good_id),1,0)
    print(good_id)
    return response

 #删除购物车所有商品   
@login_decorate    
def remove_chart_all(request,util,username):
    response = redirect('/view_chart')
    cookie_list = util.deal_cookies(request)
    print('------cookie_list-----')
    print(cookie_list)
    for key in cookie_list:
        response.set_cookie(str(key),1,0)
    return response


#修改购物车车中的商品数量
@login_decorate
def update_chart(request,util,username,good_id):
    print(good_id)
    good = Goods.objects.filter(id=good_id)
    print('||||||||||###||||||||')
    print(good)
   # good = get_object_or_404(Goods, id=good_id)

    count = (request.POST.get('count','')).strip()
    response = redirect('/view_chart')
    response.set_cookie(str(good_id),count,60*60*24)
    print('|||||||||||||||||||')
    print(count)
    return response

#生成订单第一步选择地址
@login_decorate
def view_address(request,util,username):
    user_list = User.objects.get(username=username)
    address_list=Address.objects.filter(user_id=user_list.id)
    print(address_list)
    print('===========')
    return render(request,'goods/view_address.html',{'address_list':address_list})
#第二步生成订单
@login_decorate
def create_order(request,util,username):
    user_list=User.objects.get(username=username)
    #从前端得到收获地址
    address_id = (request.POST.get('address','')).strip()
    #判断地址是否有效，是否传来地址（暂且跳过这一步）
    #将地址,支付状态写入总订单数据库中
    orders=Orders()
    orders.address_id = int(address_id)
    #将字符串改为数字整型
    orders.status=False
    orders.save()
    #将购物车中的每个商品订单写入
    orders_id = orders.id
    cookie_list=util.deal_cookies(request)
    #{'12': '4', '8': '1', '6': '1'}
    for good in cookie_list:
        #创建单个订单
        order = Order()
        order.order_id = orders_id
        order.user_id = user_list.id
        order.goods_id = good
        order.count = int(cookie_list[good])
        order.save()
    #到这里所有的加入cookie的商品都被加入到order数据库中删去所有的cookie
    response = redirect('/view_order/'+str(orders_id))
    for key in cookie_list:
        response.set_cookie(str(key),1,0)

    return response

#显示订单
@login_decorate
def view_order(request,util,username,orders_id):
    #获取总订单信息
    orders_list = Orders.objects.get(id = orders_id)
    #获取收获地址信息 包含address\phone
    orders_address_list =Address.objects.get(id = orders_list.address_id)
    #获取地址
    address=orders_address_list.address
    #从数据库中根据orders的主键对应的order外键获取每个order
    order_list = Order.objects.filter(order_id=orders_list.id)
    #获取单个订单对象 并加入到总订单orders_list_var的列表中
    orders_list_var=[]
    prices = 0
    print(address)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    for key in order_list:
        #在object中创建单个订单类对象，通过util方法给对象传递属性，
        order_object = util.set_order_list(key)
        orders_list_var.append(order_object)
        prices += order_object.price * order_object.count
        print(order_object.price)
    print(prices)
    print('------prince------')
   # return HttpResponse('ok')
    return render(request,'goods/view_order.html',{'username':username,'address':address,'orders_list_var':orders_list_var,'prices':str(prices),'orders_list':orders_list})

#查看所有订单
#将每个订单放入到一个列表中
@login_decorate
def view_all_chart(request,util,username):
    #从数据库得到所有总订单
    orders_all = Orders.objects.all()
    ALL_orders_list = []
    #遍历所有总订单得到每个总订单orders包含的商品信息order_all（即order）
    for orders in orders_all:
        order_all = Order.objects.filter(order_id = orders.id)
        #此时得到的为order表中的多个或一个，为列表,并且得到此时order表对应的用户
       # name = User.objects.get(id=(order_all[0].user_id))
      #  if name == username:
            #将没问题的多个订单orders 汇总为一个orders_object
            #同388-397行，生成一个order订单,生成一个ordes对象
        orders_object = util.set_orders_list(orders)
        orders_object_var = []
        prices = 0
        for key in order_all:
            order_object = util.set_order_list(key)
            orders_object_var.append(order_object)
            prices += order_object.price * key.count
            order_object.set_prices(prices)
        ALL_orders_list.append({orders_object:orders_object_var})
    print(ALL_orders_list)
    #all-orders_list [{orders1:[order1,order2....]},{orders2:[order3,order4...]},.......]
    #return HttpResponse('ok')
    return render(request,'goods/view_all_chart.html',{'username':username,'ALL_orders_list':ALL_orders_list})

#删除订单

@login_decorate
def delete_orders(request,util,username,orders_id,sign):
    print(orders_id)
    print('~~~~~~~~~~~~~~~~~~~~~~')
    print(sign)
    if sign =='1' or sign =='3':
        order_filter = Order.objects.get(id = orders_id)
        orders_filter = Orders.objects.get(id = order_filter.order_id)
        Order.objects.filter(id = orders_id).delete()
        A = Order.objects.filter(order_id = order_filter.id)
        if len(A)==0 :
            Order.objects.filter(id = orders_filter.id).delete()
            if sign =='3':
                response = redirect('/goods_view')
            if sign =='1':
                response=redirect('/view_all_chart')
        elif sign =='3':   
            response=redirect('/view_order/'+orders_filter.id)
    if sign =='2':
        Order.objects.filter(order_id = orders_id).delete()
        Orders.objects.filter(id = orders_id).delete()
        response = redirect('/view_all_chart')
    return response