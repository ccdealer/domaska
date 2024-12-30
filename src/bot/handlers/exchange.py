import json
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message , callback_query, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from src.bot.states import ExchangeStates
import aiofiles
from src.settings.base import VOLUME
from src.bot.keyboards import get_currency_keyboard


exchange_router = Router()


@exchange_router.callback_query(ExchangeStates.action_request)
async def select_currency(callback: callback_query, state:FSMContext):
    await state.update_data(data={"action": callback.data})
    markup= get_currency_keyboard()
    await state.set_state(state=ExchangeStates.currency_request)
    await callback.message.answer(text="Выберите валюту", reply_markup=markup)


@exchange_router.callback_query(ExchangeStates.currency_request)
async def currency_request(callback: callback_query, state: FSMContext):
    async with aiofiles.open(file=VOLUME + f"{callback.data}.json", mode="r") as f:
        temp = await f.read()
        data = json.loads(temp)

    markup = get_currency_keyboard(currency_to_remove=callback.data)
    await state.update_data(data={"data": data, "currency": callback.data})
    await state.set_state(state=ExchangeStates.exchange_currency)
    await callback.message.answer(text="Какую валюту вы хотите купитиь/продать?", reply_markup = markup)

@exchange_router.callback_query(ExchangeStates.exchange_currency)
async def exchange_currency(callback:callback_query, state:FSMContext):
    await state.update_data(data={"new currency": callback.data})
    await state.set_state(state=ExchangeStates.wait_sum)
    await callback.message.answer(text = "Введите количество валюты")



@exchange_router.message(ExchangeStates.wait_sum)
async def wait_sum(message:Message, state: FSMContext):
    try:
        text = int(message.text)
        data:dict = await state.get_data()
        action:str = data.get("action")
        rate:dict = data.get("data")
        current_currency:str = data.get("currency")
        new_currency:str = data.get("new currency")
        coeficent: float = rate.get(new_currency)
        coeficent1:float = rate.get(current_currency)
        if action == "BUY":
            await message.answer(text=f"{text * coeficent}")
        elif action == "SALE":
            await message.answer(text=f"Вам нужно {text * coeficent1} {new_currency} для покупки {text} {current_currency}  ")
    except Exception:
        await message.answer(text="Введите корректное число.")

