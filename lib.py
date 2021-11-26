from transitions import Machine

# создаём форму и указываем поля

class pizza(object):

    states = ['asleep', 'OKsizePizza', 'OKpay', 'OKcomfirmOrder']
    orderNow = {"size":"", "pay":""}
    question = ""
    
    def __init__(self, name):
        self.name = name
        self.machine = Machine(model=self, states=pizza.states, initial='asleep')
        self.machine.add_transition(trigger='whatPizza', source='asleep', dest='OKsizePizza', after='quiestSizePizza')
        self.machine.add_transition(trigger='howPay', source='OKsizePizza', dest='OKpay', after='quiestPay')
        self.machine.add_transition(trigger='comfirmOrder', source='OKpay', dest='OKcomfirmOrder', after='quiestComfirmOrder')
        self.machine.add_transition(trigger='finish', source='OKcomfirmOrder', dest='asleep', after='quiestFinish')
        self.machine.add_transition('nap', '*', 'asleep')

    def quiestSizePizza(self):
        self.question = "Какую вы хотите пиццу? Большую или маленькую?"

    def quiestPay(self):
        self.question = "Как вы будете платить?"

    def quiestComfirmOrder(self):
        self.question = "Вы хотите {sizePizza} пиццу, оплата - {howPay}?".format(sizePizza=self.orderNow["size"], howPay=self.orderNow["pay"])

    def quiestFinish(self):
        self.question = "Спасибо за заказ!"
        self.orderNow = {"size":"", "pay":""}
