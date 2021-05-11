from hw2 import Order


def test_discount_program():
    # Testing different discount programs.
    def morning_discount(order):
        order.discount = 0.15

    def elder_discount(order):
        order.discount = 0.20

    order_1 = Order(100, morning_discount)
    order_2 = Order(100, elder_discount)
    assert order_1.final_price() == 85 and order_2.final_price() == 80


def test_no_discount_program():
    # Testing when there's no discount program.
    order = Order(100)
    assert order.final_price() == 100
