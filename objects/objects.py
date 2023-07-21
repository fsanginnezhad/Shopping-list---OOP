from models.models import (
    DataBaseJson,
    Basket,
    Group,
    App
)

try:
    database = DataBaseJson('basket_list')
    basket_list = database.readable()
except:
    basket_list = {}
basket = Basket(basket_list)
group = Group(basket.name)
app = App(basket.name)
