from transitions import Machine

dialog = {  'whatPizza': {'question':"Какую вы хотите пиццу? Большую или маленькую?", 'answer':["большую", "маленькую"]},
            'howPay': {'question':'Как вы будете платить?', 'answer':["наличными", "картой"]},
            'comfirmOrder': {'question':'Вы хотите {sizePizza} пиццу, оплата - {howPay}?', 'answer':["да", "нет"]},
            'finish':{'question':'Спасибо за заказ!', 'answer':""}}


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
        self.machine.add_transition(trigger='nap', source='*', dest='asleep', after='quiestFinish')

    def checkSizePizza(self):
        return self.orderNow["size"] in dialog['whatPizza']['answer']

    def checkPay(self):
        return self.orderNow["pay"] in dialog['howPay']['answer']

    def checkComfirmOrder(self):
        return self.orderNow["comfirm"] in dialog['comfirmOrder']['answer']

    def quiestFinish(self):
        self.orderNow = {"size":"", "pay":"", "comfirm":""}
