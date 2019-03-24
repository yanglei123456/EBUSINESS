#购物车模型
class Chart_list():
    def set_id(self,id):
    	self.id = id
    def set_name(self,name):
    	self.name = name
    def set_price(self,price):
    	self.price = price
    def set_count(self,count):
    	self.count = count

#订单类型
class Order_list():
    def set_id(self,id):
        self.id = id
    def set_good_id(self,good_id):
        self.good_id = good_id
    def set_name(self,name):
        self.name=name
    def set_price(self,price):
        self.price=price
    def set_count(self,count):
        self.count=count
    def set_prices(self,prices):
        self.prices=prices

#总订单的模型
class Orders_list():
    def set_id(self,id):
        self.id=id
    def set_address(self,address):
        self.address = address
    def set_create_time(self,create_time):
        self.create_time = create_time
#    def set_prices(self,prices):
 #       self.prices = prices
