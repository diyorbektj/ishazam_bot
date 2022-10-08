import logging
from aiogram import Bot, Dispatcher
from shazamio import Shazam

API_TOKEN = '5118019905:AAGSkSbra_F2n3VnBalBc_D7PdaGINm72Xo'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
shazam = Shazam()
