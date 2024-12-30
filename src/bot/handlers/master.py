from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message , InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from src.bot.states import ExchangeStates , WeatherStates, JokingStates
from src.settings.base import  logger

master_router = Router()

@master_router.message(CommandStart())
async def start_comand(message: Message):
    await message.answer(text="Test BOT")

@master_router.message(Command("exchange"))
async def select_currency(message: Message, state:FSMContext):
    sale = InlineKeyboardButton(text="SALE", callback_data="SALE")
    buy = InlineKeyboardButton(text="BUY", callback_data="BUY")
    markup = InlineKeyboardMarkup(inline_keyboard = [[sale],[buy]])
    await state.set_state(state=ExchangeStates.action_request)
    await message.answer(text="Выберите валюту", reply_markup=markup)


@master_router.message(Command("wheather"))
async def select_type(message:Message, state:FSMContext):
    current = InlineKeyboardButton(text="Current", callback_data="Current")
    forecast = InlineKeyboardButton(text="Forecast", callback_data="Forecast")
    markup = InlineKeyboardMarkup(inline_keyboard=[[current],[forecast]])
    await state.set_state(state=WeatherStates.current_or_forcast)
    await message.answer(text="Выберите тип прогноза погод", reply_markup=markup)

@master_router.message(Command("joke"))
async def agreement(message:Message, state:FSMContext):
    yes = InlineKeyboardButton(text="Yes", callback_data="Yes")
    no = InlineKeyboardButton(text="No", callback_data="No")
    markup = InlineKeyboardMarkup(inline_keyboard=[[yes],[no]])
    await state.set_state(state=JokingStates.agremment_to_get_a_joke)
    logger.info(msg="123")
    await message.answer(text="Do you agree to get a random joke", reply_markup=markup)
