import config
import os
from misc import dp, bot
from . import keyboards
from . import json_methods
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import text, link
from aiogram.dispatcher.filters.state import State, StatesGroup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db.json")

class MakeNewPost(StatesGroup):
	waiting_for_head_text = State() #ждем заголовок текста
	waiting_for_body_text = State() #ждем основной текст
	waiting_for_post_img = State() #ждем фото для поста

@dp.callback_query_handler(lambda c: c.data == 'return_to_start')
@dp.message_handler(commands=['create_new_post'], state="*")
async def create_new_post_command(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.from_user.id)
	message_text = ('Отлично, сейчас с тобой мы создадим новый пост.\n' + 
					'Отправт мне заголовок твоего поста.')
	await MakeNewPost.waiting_for_head_text.set()
	await bot.send_message(callback_query.from_user.id, message_text, reply_markup=keyboards.creation_disagreement_kb)

@dp.message_handler(state=MakeNewPost.waiting_for_head_text, content_types=types.ContentTypes.TEXT)
async def post_step_1(message: types.Message, state: FSMContext):
	message_text = 'Так, теперь напиши основной текст твоего поста.'

	data = json_methods.read(DB_PATH)
	await bot.send_message(message.from_user.id,data['user_id'][message.from_user.id]['head'])
	data['user_id'][message.from_user.id] = {'head':message.text,'body':None,'photo_id':None}
	json_methods.write(DB_PATH, data)

	await MakeNewPost.next()
	await bot.send_message(message.from_user.id, message_text, reply_markup=keyboards.canceling_kb)

@dp.message_handler(state=MakeNewPost.waiting_for_body_text, content_types=types.ContentTypes.TEXT)
async def post_step_2(message: types.Message, state: FSMContext):
	message_text = 'Остался послежний шаг. Отправь мне фотографию для поста.'

	data = json_methods.read(DB_PATH)
	data['user_id'][message.from_user.id]['body'] = message.text
	json_methods.write(DB_PATH, data)

	await MakeNewPost.next()
	await bot.send_message(message.from_user.id, message_text, reply_markup=keyboards.canceling_kb)


@dp.message_handler(state=MakeNewPost.waiting_for_post_img, content_types=types.ContentTypes.PHOTO)
async def post_step_3(message: types.Message, state: FSMContext):
	message_text = 'Готово. Сейчас можно проверить корректность поста перед отправкой.'

	data = json_methods.read(DB_PATH)
	data['user_id'][message.from_user.id]['photo_id'] = message.photo[0].file_id
	json_methods.write(DB_PATH, data)

	await state.finish()
	await bot.send_message(message.from_user.id, message_text, reply_markup=keyboards.review_post_kb)

@dp.callback_query_handler(lambda c: c.data == 'review_post')
async def review_new_post(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.from_user.id)
	data = json_methods.read(DB_PATH)
	message_text = data['user_id'][callback_query.from_user.id]['head'] + '\n\n' + data['user_id'][callback_query.from_user.id]['body']

	await bot.send_photo(callback_query.from_user.id, data['user_id'][callback_query.from_user.id]['photo_id'], caption = message_text, reply_markup = keyboards.agreement_to_send_post_kb)

@dp.callback_query_handler(lambda c: c.data == 'send_post_to_chanel')
async def send_new_post(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.from_user.id)
	await bot.send_photo(config.CHANEL_ID, data['user_id'][callback_query.from_user.id]['photo_id'], caption = message_text, reply_markup = keyboards.agreement_to_send_post_kb)
	message_text = text('Готово, ваш пост был отправлен в ' + 
						link('канал.', config.CHANEL_URL) + 
						'\nХотите создать еще один пост?')
	await bot.send_message(callback_query.from_user.id, message_text, reply_markup = creation_agreement_kb, parse_mode = ParseMode.MARKDOWN)

#ловим мусор
@dp.message_handler(content_types=types.ContentType.ANY)
async def unknown_message(message: types.Message):
	message_text = 'Кажется что-то пошло не так. Попробуй еще раз.'
	await bot.send_message(message.from_user.id, message_text)
