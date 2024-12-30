from aiogram.fsm.state import State, StatesGroup

class ExchangeStates(StatesGroup):
    currency_request = State()
    exchange_currency = State()
    wait_sum = State()
    action_request = State()

class WeatherStates(StatesGroup):
    current_or_forcast = State()
    request_days = State()
    request_city_current = State()
    request_city_forecast = State()


class JokingStates(StatesGroup):
    agremment_to_get_a_joke = State()


