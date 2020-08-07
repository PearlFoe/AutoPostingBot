import os
import config
import aiohttp
import handlers
import logging

from aiogram import Bot, types
from misc import dp, bot
from aiogram.utils import executor
from aiogram.utils.executor import start_webhook
from aiogram.dispatcher.webhook import get_new_configured_app

PROJECT_NAME = 'evening-woodland-92421'

WEBHOOK_HOST = f'https://{PROJECT_NAME}.herokuapp.com'
WEBHOOK_URL_PATH = f'/webhook/{config.TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_URL_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT')

async def on_startup(app):
	await bot.delete_webhook()
	await bot.set_webhook(WEBHOOK_URL)
	
async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')

if __name__ == '__main__':
	if "HEROKU" in list(os.environ.keys()):	
		start_webhook(
		dispatcher=dp,
		webhook_path=WEBHOOK_URL_PATH,
		on_startup=on_startup,
		on_shutdown=on_shutdown,
		skip_updates=True,
		host=WEBAPP_HOST,
		port=WEBAPP_PORT,
	    	)
	else:
		executor.start_polling(dp)
