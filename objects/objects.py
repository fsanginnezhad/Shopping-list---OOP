from models.models import (
    DataBaseJson,
    Basket,
    Group
)

try:
    database = DataBaseJson('basket_list')
    basket_list = database.readable()
except:
    basket_list = {}
basket = Basket(basket_list)
group = Group(basket.name)
