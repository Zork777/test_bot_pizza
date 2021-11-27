import multiprocessing
import time
import datetime


from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lib import pizza, dialog
from test import test

token = '1941337133:AAF5wC8XiHQlLeC2NEPc-Zd7UaIu59jAr54' 
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# создаём форму и указываем поля
class FormPizza(StatesGroup):
    size = State() 
    pay = State()
    comfirm = State()
    pizzaOrder = pizza('PIZZA') 

startKey = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('сделать заказ'))

pizzaSizeKey = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('большую')).add(
    KeyboardButton('маленькую')).add(
    KeyboardButton('отмена'))

payKey = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('наличными')).add(
    KeyboardButton('картой')).add(
    KeyboardButton('отмена'))

YesNoKey = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('да')).add(
    KeyboardButton('нет'))


# Ловим Help
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer('Чтобы сделать заказ наберите команду /start', reply_markup=startKey)


# Начинаем наш диалог
@dp.message_handler(commands=['start'])
@dp.message_handler(Text(equals='сделать заказ', ignore_case=True), state='*')
async def cmd_start(message: types.Message):
    print (message)
    await FormPizza.size.set()
    await message.answer(dialog['whatPizza'], reply_markup=pizzaSizeKey)


# Добавляем возможность отмены, если пользователь передумал заполнять
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    FormPizza.pizzaOrder.nap()
    await state.finish()
    await message.answer('Ордер отменен')


# Сюда приходит ответ с размером пиццы
@dp.message_handler(state=FormPizza.size)
async def process_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        FormPizza.pizzaOrder.orderNow['size'] = message.text
        if FormPizza.pizzaOrder.whatPizza():
            await FormPizza.next()
        else:
            return await message.answer('Выбери размер пиццы или отмени', reply_markup=pizzaSizeKey)

#следующий вопрос, как будем платить?    
    await message.answer(dialog['howPay'], reply_markup=payKey)


# Принимаем вид платежа, выводим и подтверждаем ордер
@dp.message_handler(state=FormPizza.pay)
async def process_pay(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        FormPizza.pizzaOrder.orderNow['pay'] = message.text
        if FormPizza.pizzaOrder.howPay():
            await FormPizza.next()
        else:
            return await message.answer('Выбери форму оплаты или отмени', reply_markup=payKey)
#следующий вопрос, подтверждение ордера
    await message.answer(dialog['comfirmOrder'].format(sizePizza=FormPizza.pizzaOrder.orderNow["size"],
                                                        howPay=FormPizza.pizzaOrder.orderNow["pay"]),
                                                        reply_markup=YesNoKey)


# Принимаем подтверждение ордера
@dp.message_handler(state=FormPizza.comfirm)
async def process_pay(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        FormPizza.pizzaOrder.orderNow['comfirm'] = message.text
        if FormPizza.pizzaOrder.comfirmOrder():
            if message.text.lower() in 'нет' in message.text:
                await message.answer('Ордер отменен')
            else:
                FormPizza.pizzaOrder.finish()
                await bot.send_message(message.chat.id, dialog['finish'])
        else:
            return await message.answer('Укажи Да или Нет кнопкой на клавиатуре', reply_markup=YesNoKey)

    FormPizza.pizzaOrder.nap()
    await state.finish()


# Ловим все оставшиеся сообщения
@dp.message_handler()
async def all_message(message: types.Message):
    await message.answer('нажмите на кнопку, чтобы сделать заказ', reply_markup=startKey)


def main_flow():
  #start bot
    print ('start bot pizza...')
    executor.start_polling(dp, skip_updates=True)

#контроль работы бота, в случае падения рестарт    
def start():
    t_bot_flow = multiprocessing.Process(name = 'bot_flow', target=main_flow)
    
    t_bot_flow.start()
    while 1:
        if not t_bot_flow.is_alive():
            print ('restart bot flow in Telegramm...')
            t_bot_flow.kill()
            t_bot_flow.terminate()
            t_bot_flow = multiprocessing.Process(
                            name = 'bot_flow',
                            target=main_flow)
            t_bot_flow.start()
        time.sleep(1)
        print ('telegram bot pizza{:>100}\r'.format(datetime.datetime.now().isoformat()), end='\r')  


if __name__ == '__main__':
    # test() # тест диалога
    start()


    