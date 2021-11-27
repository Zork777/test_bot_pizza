import sys
from lib import pizza, dialog

def test():
    print ('start test')
    pizzaOrder = pizza("PIZZA")
    print (f'order-{pizzaOrder.orderNow}')
    print (f'state- {pizzaOrder.state}\n')


    print (dialog['whatPizza']['question'] )
    pizzaOrder.orderNow["size"] = "большую"
    if pizzaOrder.whatPizza():
        print (f'order now-{pizzaOrder.orderNow}')    
        print (f'state- {pizzaOrder.state}\n')
    else:
        print ("ошибка в ответе размера пиццы")
        sys.exit(1)

    print (dialog['howPay']['question'])
    pizzaOrder.orderNow["pay"] = "наличными"
    if pizzaOrder.howPay():
        print (f'order now-{pizzaOrder.orderNow}')    
        print (f'state- {pizzaOrder.state}\n')
    else:
        print ("ошибка в ответе формы оплаты")
        sys.exit(1)    

    print (dialog['comfirmOrder']['question'].format(sizePizza=pizzaOrder.orderNow["size"], howPay=pizzaOrder.orderNow["pay"]))
    pizzaOrder.orderNow["comfirm"] = "да"
    if pizzaOrder.comfirmOrder():
        print (f'order now-{pizzaOrder.orderNow}')    
        print (f'state- {pizzaOrder.state}\n')
    else:
        print ("ошибка в ответе подтверждения ордера")
        sys.exit(1)       

    print (dialog['finish']['question'])
    pizzaOrder.finish()
    print (f'order now-{pizzaOrder.orderNow}')    
    print (f'state- {pizzaOrder.state}\n')
    print ('test finish')
