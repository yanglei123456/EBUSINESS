from django.contrib import admin
from goods.models import User,Goods,Address,Orders,Order
# Register your models here.
class User_admin(admin.ModelAdmin):
    list_display=['username','email','password']
admin.site.register(User,User_admin) 

class Goods_admin(admin.ModelAdmin):
    list_display=['name','price','picture','desc']
admin.site.register(Goods,Goods_admin)

class User_address_message(admin.ModelAdmin):
    list_display=['user','address','phone']
admin.site.register(Address,User_address_message)
