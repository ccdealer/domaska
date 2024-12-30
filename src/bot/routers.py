from src.bot.handlers.master import master_router
from src.bot.handlers.exchange import exchange_router
from src.bot.handlers.weather import wheather_router
from src.bot.handlers.jokes import jocking_router

ROUTERS = [
    master_router,
    exchange_router,
    wheather_router,
    jocking_router
]