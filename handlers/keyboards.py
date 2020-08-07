from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

#кнопка для создания нового поста
send_post_data_btn = InlineKeyboardButton('Создать новый пост', callback_data = 'creation_agreement')

#кнопка отправки готового поста
send_post_to_chanel_btn = InlineKeyboardButton('Отправить пост', callback_data = 'send_post_to_chanel')

#кнопка проверки поста
review_post_btn = InlineKeyboardButton('Проверить пост', callback_data = 'review_post')

#кнопк возврата в начало и отмены создания поста
return_to_start_btn = InlineKeyboardButton('Вернуться в начало', callback_data = 'return_to_start')
canceling_btn = InlineKeyboardButton('Отменить создание поста', callback_data = 'cancel_post_creation')



#клавиатура создания нового поста
creation_agreement_kb = InlineKeyboardMarkup()
creation_agreement_kb.add(send_post_data_btn)

#клавиатура отмены создания поста
creation_disagreement_kb = InlineKeyboardMarkup()
creation_disagreement_kb.add(canceling_btn)

#клавиатура отмены действия
canceling_kb = InlineKeyboardMarkup()
canceling_kb.add(return_to_start_btn)
canceling_kb.add(canceling_btn)

#клавиатура проверки/отправки поста
review_post_kb = InlineKeyboardMarkup()
review_post_kb.add(review_post_btn)
review_post_kb.add(send_post_to_chanel_btn)

#клавиатура отправки поста
send_post_to_chanel_kb = InlineKeyboardMarkup()
send_post_to_chanel_kb.add(send_post_to_chanel_btn)

#клавиатура согласия на отправку поста
agreement_to_send_post_kb = InlineKeyboardMarkup()
agreement_to_send_post_kb.add(send_post_to_chanel_btn)
agreement_to_send_post_kb.add(return_to_start_btn)
agreement_to_send_post_kb.add(canceling_btn)
