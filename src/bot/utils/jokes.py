from aiohttp import ClientSession
# from src.settings.base import  logger
from src.settings.base import  logger


BASE_URL = "https://official-joke-api.appspot.com/random_joke"


async def get_a_joke():
    url = BASE_URL
    async with ClientSession() as session:
        try:
            response = await session.get(url=url)
            print(response)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Something went wrong during function {__name__}: {e}")
            return None
        data: dict = await response.json()
    jokes = data.get("setup")
    jokes1 = data.get("punchline")
    logger.info(jokes1)
    jokes3 = [jokes,jokes1]
    return jokes3




