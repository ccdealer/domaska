
from aiohttp import ClientSession

# Local
from src.settings.base import API_WEATHER_KEY, logger


BASE_URL = "http://api.weatherapi.com/v1"
CURRENT = "/current.json"
FORECAST = "/forecast.json"

async def get_current_weather(city_name:str):
    url = (f"{BASE_URL}{CURRENT}?key={API_WEATHER_KEY}&q={city_name}&aqi=no")
    async with ClientSession() as session:
        try:
            response = await session.get(url=url)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Something went wrong during function {__name__}: {e}")
            return None
        data: dict[dict] = await response.json()
    current = data.get("current")
    return current

async def get_weather_forcast(city_name:str, days:int):
    url = (f"{BASE_URL}{FORECAST}?key={API_WEATHER_KEY}&q={city_name}&days={days}&aqi=no")
    async with ClientSession() as session:
        try:
            response = await session.get(url=url)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Something went wrong during function {__name__}: {e}")
            return None
        data: dict[dict] = await response.json()
    forecast = data.get("forecast")
    return forecast