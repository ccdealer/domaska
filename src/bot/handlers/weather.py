import json
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message , callback_query, CallbackQuery
from aiogram.fsm.context import FSMContext
from src.bot.states import WeatherStates
from src.bot.utils.weather import get_current_weather, get_weather_forcast


wheather_router = Router()

@wheather_router.callback_query(WeatherStates.current_or_forcast, F.data == "Current")
async def request_for_city_current(callback: CallbackQuery, state: FSMContext):
    await state.update_data(data={"status": callback.data})
    await state.set_state(state=WeatherStates.request_city_current)
    await callback.message.answer(text="Введите название города")

@wheather_router.callback_query(WeatherStates.current_or_forcast, F.data == "Forecast")
async def request_for_days_forecast(callback: CallbackQuery, state: FSMContext):
    await state.update_data(data={"days": (callback.data+"asf")})
    await state.set_state(state=WeatherStates.request_days)
    await callback.message.answer(text="Введите на сколько дней вперёд предсказать погоду")

@wheather_router.message(WeatherStates.request_days)
async def request_for_city_forecast(message:Message, state: FSMContext):
    await state.update_data(data={"status": message.text})
    await state.set_state(state=WeatherStates.request_city_forecast)
    await message.answer(text="Введите название города")




@wheather_router.message(WeatherStates.request_city_current)
async def wait_city_current(message:Message, state: FSMContext):
    data = await state.get_data()
    status = data.get("status")
    current_wheather = await get_current_weather(city_name=message.text)
    if not current_wheather:
        await message.answer(text="Что то пошло не так")
    else:
        temp = current_wheather["temp_c"]
        condition = current_wheather["condition"]["text"]
        wind = current_wheather["wind_kph"]
        humidity = current_wheather["humidity"]
        template = f""" температура - {temp}
    condition - {condition}
    wind - {wind}
    humidity - {humidity} 
bbbbbbbbbbbbbbbbbbbbb"""
    await state.clear()
    await message.answer(text=template)


@wheather_router.message(WeatherStates.request_city_forecast)
async def wait_city_current(message:Message, state: FSMContext):
    data = await state.get_data()
    status:int = int(data.get("status")) + 2
    wheather_forcast = await get_weather_forcast(city_name=message.text, days=status)
    if not wheather_forcast:
        await message.answer(text="Что то пошло не так ASD")
    else:
        data = wheather_forcast["forecastday"][status-2]["date"]
        temp = wheather_forcast["forecastday"][status-2]["day"]["avgtemp_c"]
        condition = wheather_forcast["forecastday"][status-2]["day"]["condition"]["text"]
        wind = wheather_forcast["forecastday"][status-2]["day"]["maxwind_kph"]
        humidity = wheather_forcast["forecastday"][status-2]["day"]["avghumidity"]
        template = f""" 
        datint(a ======= {data})
        температура - {temp}
        condition - {condition}
        wind - {wind}
        humidity - {humidity} 
    aaaaaaaaaaaaaaaaaaaaaaa"""
        await state.clear()
        await message.answer(text=template)
