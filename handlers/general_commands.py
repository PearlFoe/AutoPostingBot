from aiogram import types
from misc import dp, bot

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
	message_text = ('Привет!\n' +
					'Это бот-помощник для автопостинга товаров в канал.\n' +
					'Напиши /help, чтобы получить список возможных команд.')
	await bot.send_message(message.from_user.id, message_text)

@dp.message_handler(commands=['help'])
async def send_commands_list(message: types.Message):
	message_text = ('/start - начать общение с ботом\n' +
					'/help - вывод списка команд\n' +
					'/create_new_post - отправить данные о товаре в канал\n' +
					'/exit - завершить общение с ботом')
	await bot.send_message(message.from_user.id,message_text)

@dp.message_handler(commands=['exit'])
async def exit_command(message: types.Message):
	message_text = 'Буду ждать вашего возвращения. Если захотите возобновить диалог, просто напишите /start.'
	await bot.send_message(message.from_user.id, message_text)
