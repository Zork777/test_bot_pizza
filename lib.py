from transitions import Machine

dialog = {  'whatPizza':"Какую вы хотите пиццу? Большую или маленькую?",
            'howPay':'Как вы будете платить?',
            'comfirmOrder':'Вы хотите {sizePizza} пиццу, оплата - {howPay}?',
            'finish':'Спасибо за заказ!'}


# создаём форму и указываем поля
class pizza(object):

    states = ['asleep', 'OKsizePizza', 'OKpay', 'OKcomfirmOrder']
    orderNow = {"size":"", "pay":"", "comfirm":""}
    
    def __init__(self, name):
        self.name = name
        self.machine = Machine(model=self, states=pizza.states, initial='asleep')
        self.machine.add_transition(trigger='whatPizza', source='asleep', dest='OKsizePizza', conditions=['checkSizePizza'])
        self.machine.add_transition(trigger='howPay', source='OKsizePizza', dest='OKpay', conditions=['checkPay'])
        self.machine.add_transition(trigger='comfirmOrder', source='OKpay', dest='OKcomfirmOrder', conditions=['checkComfirmOrder'])
        self.machine.add_transition(trigger='finish', source='OKcomfirmOrder', dest='asleep', after='quiestFinish')
        self.machine.add_transition('nap', '*', 'asleep')

    def checkSizePizza(self):
        return self.orderNow["size"] in ["большую", "маленькую"]

    def checkPay(self):
        return self.orderNow["pay"] in ["наличными", "картой"]

    def checkComfirmOrder(self):
        return self.orderNow["comfirm"] in ["да", "нет"]

    def quiestFinish(self):
        self.question = "Спасибо за заказ!"
        self.orderNow = {"size":"", "pay":""}
