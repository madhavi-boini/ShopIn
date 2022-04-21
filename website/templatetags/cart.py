from django import template

register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False


@register.filter(name='product_quantity')
def product_quantity(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0

@register.filter(name='product_price')
def product_price(product,cart):
    cost=int(product.cost)
    discount=int(product.discount)
    price = (cost-cost*discount/100)*product_quantity(product, cart)
    price = round(price,2)
    return price

@register.filter(name='total_cost')
def total_cost(products,cart):
    totalCost=0
    for product in products:
         totalCost+=product_price(product,cart)
    totalCost=round(totalCost,2)
    return totalCost

@register.filter(name='price')
def price(product):
    cost=int(product.cost)
    discount=int(product.discount)
    price = (cost-cost*discount/100)
    price = round(price,2)
    return price
