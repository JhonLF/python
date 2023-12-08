from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

money_machine = MoneyMachine()
coffe_maker = CoffeeMaker()
menu = Menu()
machine_on = True

while machine_on:
    print("Welcome to Coffe Machine\n")
    order_name = input("What would you like?\n" + menu.get_items()+":\n").lower()
    if order_name == "off":
        machine_on = False
    elif order_name == "report":
        coffe_maker.report()
        money_machine.report()
    else:
        order = menu.find_drink(order_name)
        if coffe_maker.is_resource_sufficient(order) and money_machine.make_payment(order.cost):
            coffe_maker.make_coffee(order)













