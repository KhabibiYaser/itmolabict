import telebot
import random
from telebot import types

TOKEN = '7137150561:AAFdHVcd6iv6veSxNIhtm4btdnO5Jjt1SE0'
bot = telebot.TeleBot(TOKEN)

# Словарь с цитатами, разделённый по темам и персонажам
quotes = {
    '💼 Бизнес': {
        'Стив Джобс 🖥️': [
            "«Время — бесценный капитал.»\n\n— Стив Джобс 🖥️",
            "«Будь мерилом качества. Некоторые люди не привыкли к среде, где ожидается совершенство.»\n\n— Стив Джобс 🖥️",
            "«Инновации отличают лидера от догоняющего.»\n\n— Стив Джобс 🖥️"
        ],
        'Уоррен Баффет 💰': [
            "«Правило номер один: никогда не теряйте деньги. Правило номер два: никогда не забывайте правило номер один.»\n— Уоррен Баффет 💰",
            "«Лучшее вложение — это вложение в себя.»\n\n— Уоррен Баффет 💰",
            "«Покупайте страх, продавайте жадность.»\n\n— Уоррен Баффет 💰"
        ]
    },
    '🗳️ Политика': {
        'Уинстон Черчилль 🇬🇧': [
            "«Успех — это способность двигаться от одной неудачи к другой, не теряя энтузиазма.»\n\n— Уинстон Черчилль 🇬🇧",
            "«История будет добра ко мне, потому что я собираюсь писать ее сам.»\n\n— Уинстон Черчилль 🇬🇧",
            "«Лучший аргумент против демократии — пятиминутный разговор с обычным избирателем.»\n\n— Уинстон Черчилль 🇬🇧"
        ],
        'Нельсон Мандела ✊': [
            "«Самое трудное в жизни — это решиться начать.»\n\n— Нельсон Мандела ✊",
            "«Образование — самое мощное оружие, которое вы можете использовать, чтобы изменить мир.»\n\n— Нельсон Мандела ✊",
            "«Я никогда не проигрываю. Я либо выигрываю, либо учусь.»\n\n— Нельсон Мандела ✊"
        ]
    },
    '🔬 Наука': {
        'Альберт Эйнштейн 🧠': [
            "«Воображение важнее знания.»\n\n— Альберт Эйнштейн 🧠",
            "«Жизнь — как езда на велосипеде. Чтобы сохранить равновесие, ты должен двигаться.»\n\n— Альберт Эйнштейн 🧠",
            "«Я никогда не думаю о будущем. Оно приходит достаточно скоро.»\n\n— Альберт Эйнштейн 🧠"
        ],
        'Мария Кюри 🧪': [
            "«В жизни нет ничего страшного. Есть только то, что нужно понять.»\n\n— Мария Кюри 🧪",
            "«Надо иметь терпение и уверенность в себе. Надо верить, что всё возможно.»\n\n— Мария Кюри 🧪",
            "«Я из тех, кто верит, что наука обладает великой красотой.»\n\n— Мария Кюри 🧪"
        ]
    },
    '🧘 Духовный рост': {
        'Будда 🕉️': [
            "«Миром правит разум, а не сила.»\n\n— Будда 🕉️",
            "«Будь светом для себя.»\n\n— Будда 🕉️",
            "«Счастье — это не иметь много, а хотеть мало.»\n\n— Будда 🕉️"
        ],
        'Лао-цзы 🌿': [
            "«Путь в тысячу ли начинается с первого шага.»\n— Лао-цзы 🌿",
            "«Когда я отпускаю то, что я есть, я становлюсь тем, кем мог бы быть.»\n— Лао-цзы 🌿",
            "«Тот, кто знает людей, мудр. Тот, кто знает себя, просвещен.»\n— Лао-цзы 🌿"
        ]
    }
}

# Глоуб переменные для отслеживания текущего выбора пользователя
current_person = None
current_field = None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    intro_message = (
    "🌟 **Приветствуем в WisdomBot!** 🌟\n\n"
    "Здесь ты найдешь мудрость и советы от людей, которые изменили мир своими идеями и вдохновили меня. "
    "Эти мысли помогут тебе взглянуть на жизнь под новым углом и найти ответы на важные вопросы.\n\n"
    "**WisdomBot** создан для того, чтобы делиться с тобой знаниями великих личностей, "
    "побуждая тебя к глубоким размышлениям и новым свершениям. 📚🌟"
    )

    # Отправляем интро-сообщение при первом запуске
    bot.send_message(message.chat.id, intro_message, parse_mode='Markdown')
    # После интро отображаем клавиатуру выбора сфер
    show_spheres_keyboard(message)


# Отдельная функция для показа клавиатуры выбора сфер
def show_spheres_keyboard(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('💼 Бизнес')
    btn2 = types.KeyboardButton('🗳️ Политика')
    btn3 = types.KeyboardButton('🔬 Наука')
    btn4 = types.KeyboardButton('🧘 Духовный рост')
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, "Выберите сферу жизни:", reply_markup=markup)


# Функция для обработки выбора сферы
@bot.message_handler(func=lambda message: message.text in quotes.keys())
def choose_person(message):
    global current_field, current_person
    current_field = message.text
    current_person = None  # Сбросить выбранного персонажа при смене сферы
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for person in quotes[current_field].keys():
        markup.add(types.KeyboardButton(person))
    markup.add(types.KeyboardButton("🔙 Назад"))
    bot.send_message(message.chat.id, f"Вы выбрали {current_field}.\n\nТеперь выберите личность:", reply_markup=markup)


# Функция для обработки выбора персонажа или возврата назад
@bot.message_handler(func=lambda message: message.text in [person for field in quotes.values() for person in
                                                           field.keys()] or message.text == "🔙 Назад" or message.text == "Новая цитата")
def send_quote_or_go_back(message):
    global current_person, current_field

    if message.text == "🔙 Назад":
        # Если пользователь нажимает кнопку "Назад", показываем выбор сфер
        show_spheres_keyboard(message)

    elif message.text == "Новая цитата":
        # Проверяем, инициализированы ли current_person и current_field
        if current_person and current_field:
            # Если персонаж и тема выбраны, выводим новую цитату
            person_quotes = quotes[current_field][current_person]
            random_quote = random.choice(person_quotes)
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            markup.add(types.KeyboardButton("Новая цитата"))
            markup.add(types.KeyboardButton("🔙 Назад"))
            bot.send_message(message.chat.id, f"{random_quote}", reply_markup=markup)
        else:
            # Если персонаж или тема не выбраны, отправляем пользователя на выбор сферы
            bot.send_message(message.chat.id, "Пожалуйста, сначала выберите сферу и персонажа.")
            show_spheres_keyboard(message)

    else:
        # Если пользователь выбрал персонажа, запоминаем его и выводим цитату
        if message.text in quotes[current_field]:
            current_person = message.text
            person_quotes = quotes[current_field][current_person]
            random_quote = random.choice(person_quotes)
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            markup.add(types.KeyboardButton("Новая цитата"))
            markup.add(types.KeyboardButton("🔙 Назад"))
            bot.send_message(message.chat.id, f"{random_quote}", reply_markup=markup)
        else:
            # Если что-то пошло не так, предлагаем выбрать персонажа
            bot.send_message(message.chat.id, "Пожалуйста, выберите персонажа из списка.")
# Запуск бота
bot.polling()

#
#
# # Словарь с цитатами, разделённый по темам и персонажам
# quotes = {
#     'Бизнес': {
#         'Стив Джобс': [
#             "Время - бесценный капитал.",
#             "Будь мерилом качества. Некоторые люди не привыкли к среде, где ожидается совершенство.",
#             "Инновации отличают лидера от догоняющего."
#         ],
#         'Уоррен Баффет': [
#             "Правило номер один: никогда не теряйте деньги. Правило номер два: никогда не забывайте правило номер один.",
#             "Лучшее вложение — это вложение в себя.",
#             "Покупайте страх, продавайте жадность."
#         ]
#     },
#     'Политика': {
#         'Уинстон Черчилль': [
#             "Успех — это способность двигаться от одной неудачи к другой, не теряя энтузиазма.",
#             "История будет добра ко мне, потому что я собираюсь писать ее сам.",
#             "Лучший аргумент против демократии — пятиминутный разговор с обычным избирателем."
#         ],
#         'Нельсон Мандела': [
#             "Самое трудное в жизни — это решиться начать.",
#             "Образование — самое мощное оружие, которое вы можете использовать, чтобы изменить мир.",
#             "Я никогда не проигрываю. Я либо выигрываю, либо учусь."
#         ]
#     },
#     'Наука': {
#         'Альберт Эйнштейн': [
#             "Воображение важнее знания.",
#             "Жизнь — как езда на велосипеде. Чтобы сохранить равновесие, ты должен двигаться.",
#             "Я никогда не думаю о будущем. Оно приходит достаточно скоро."
#         ],
#         'Мария Кюри': [
#             "В жизни нет ничего страшного. Есть только то, что нужно понять.",
#             "Надо иметь терпение и уверенность в себе. Надо верить, что всё возможно.",
#             "Я из тех, кто верит, что наука обладает великой красотой."
#         ]
#     },
#     'Духовный рост': {
#         'Будда': [
#             "Миром правит разум, а не сила.",
#             "Будь светом для себя.",
#             "Счастье — это не иметь много, а хотеть мало."
#         ],
#         'Лао-цзы': [
#             "Путь в тысячу ли начинается с первого шага.",
#             "Когда я отпускаю то, что я есть, я становлюсь тем, кем мог бы быть.",
#             "Тот, кто знает людей, мудр. Тот, кто знает себя, просвещен."
#         ]
#     }
# }
#
# # Глобальные переменные для отслеживания текущего выбора пользователя
# current_person = None
# current_field = None
#
# # Функция для обработки команды /start
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#     btn1 = types.KeyboardButton('Бизнес')
#     btn2 = types.KeyboardButton('Политика')
#     btn3 = types.KeyboardButton('Наука')
#     btn4 = types.KeyboardButton('Духовный рост')
#     markup.add(btn1, btn2, btn3, btn4)
#     bot.send_message(message.chat.id, "Выберите сферу жизни:", reply_markup=markup)
#
# # Функция для обработки выбора сферы
# @bot.message_handler(func=lambda message: message.text in quotes.keys())
# def choose_person(message):
#     global current_field, current_person
#     current_field = message.text
#     current_person = None  # Сбросить выбранного персонажа при смене сферы
#     markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#     for person in quotes[current_field].keys():
#         markup.add(types.KeyboardButton(person))
#     markup.add(types.KeyboardButton("Назад"))
#     bot.send_message(message.chat.id, f"Вы выбрали {current_field}. Теперь выберите персонажа:", reply_markup=markup)
#
# # Функция для обработки выбора персонажа или возврата назад
# @bot.message_handler(func=lambda message: message.text in [person for field in quotes.values() for person in field.keys()] or message.text == "Назад" or message.text == "Новая цитата")
# def send_quote_or_go_back(message):
#     global current_person, current_field
#     if message.text == "Назад":
#         send_welcome(message)
#     elif message.text == "Новая цитата" and current_person and current_field:
#         # Проверка, что текущий персонаж и тема инициализированы
#         if current_person in quotes[current_field]: #подсловарь с персонажами и их цитатами для конкретной темы.
#             person_quotes = quotes[current_field][current_person] #это список всех цитат, принадлежащих выбранному персонажу в текущей теме.
#             random_quote = random.choice(person_quotes)
#             markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
#             markup.add(types.KeyboardButton("Новая цитата"))
#             markup.add(types.KeyboardButton("Назад"))
#             bot.send_message(message.chat.id, f"Цитата от {current_person}: {random_quote}", reply_markup=markup)
#         else:
#             bot.send_message(message.chat.id, "Произошла ошибка. Попробуйте выбрать персонажа снова.")
#     else:
#         # Запомнить выбранного персонажа и выдать первую цитату
#         if message.text in quotes[current_field]:
#             current_person = message.text
#             person_quotes = quotes[current_field][current_person]
#             random_quote = random.choice(person_quotes)
#             markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
#             markup.add(types.KeyboardButton("Новая цитата"))
#             markup.add(types.KeyboardButton("Назад"))
#             bot.send_message(message.chat.id, f"Цитата от {current_person}: {random_quote}", reply_markup=markup)
#         else:
#             bot.send_message(message.chat.id, "Пожалуйста, выберите персонажа из списка.")
#
# # Запуск бота
# bot.polling()


# import telebot
#
# bot = telebot.TeleBot("7137150561:AAFdHVcd6iv6veSxNIhtm4btdnO5Jjt1SE0", parse_mode=None)
#
#
#
# @bot.message_handler(commands=['start','wassup'])
# def send_welcome(message):
#     if message.text == "/wassup":
#         bot.reply_to(message, "Привет! че как?!")
#     else:
#         bot.reply_to(message, f"Привет! Я бот!{message.text}")
#
# @bot.message_handler(commands=['help'])
# def send_help(message):
#     bot.reply_to(message,"Чем могу быть полезен?")
#
# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     bot.reply_to(message,"чувак , введи команду /help")
#
#
# bot.polling(non_stop=True)