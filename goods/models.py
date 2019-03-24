from django.db import models

# Create your models here.
#用户模型
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    
    def __str__(self):
        return self.username

#商品模型
class Goods(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    picture = models.FileField(upload_to = 'upload',default='i')
    desc = models.TextField()
   
    def __str__(self):
        return self.name
   
#收获地址
class Address(models.Model):
    user = models.ForeignKey(User)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.address
 
#商品总订单
class Orders(models.Model):
    address = models.ForeignKey(Address)
    create_time = models.DateTimeField(auto_now=True)
    status = models.BooleanField()
    
    def __str__(self):
        return self.create_time

#单个订单
class Order(models.Model):
    order=models.ForeignKey(Orders)
    user = models.ForeignKey(User)
    goods=models.ForeignKey(Goods)
    count = models.IntegerField()
