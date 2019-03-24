#运用表单py 代替网页的表单信息
from django import forms
#定义注册表单
class UserForm(forms.Form):
    username = forms.CharField(label = '用户名',max_length=100)
    password = forms.CharField(label = '密码',widget=forms.PasswordInput())
    email = forms.EmailField(label = '邮箱')
 
#定义登录表单
class LoginForm(forms.Form):
    username = forms.CharField(label = '用户名',max_length=100)
    password = forms.CharField(label = '密码',widget=forms.PasswordInput())

#定义地址表单
class AddressForm(forms.Form):
    address = forms.CharField(label = '地址',max_length=50)
    phone = forms.CharField(label = '电话',max_length=50)


    
