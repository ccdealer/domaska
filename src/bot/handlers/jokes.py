import json
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message , callback_query, CallbackQuery
from aiogram.fsm.context import FSMContext
from src.bot.states import JokingStates
from src.bot.utils.jokes import get_a_joke
from src.settings.base import  logger




jocking_router = Router()


@jocking_router.callback_query(JokingStates.agremment_to_get_a_joke, F.data == "Yes")
async def geting_a_joke(callback: CallbackQuery, state:FSMContext):
    result = await get_a_joke()
    if not result:
        await callback.message.answer(text="Что то пошло не так")
    else:
        template= f'''{result[0]}
{result[1]}'''
        await state.clear()
        await callback.message.answer(text=template)

@jocking_router.callback_query(JokingStates.agremment_to_get_a_joke, F.data == "No")
async def geting_a_joke(callback: CallbackQuery, state:FSMContext):
    await callback.message.answer(text="Ну и не надо")