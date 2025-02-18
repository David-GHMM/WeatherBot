import telebot
import configure
import weather_parser as parser

bot = telebot.TeleBot(configure.config['token'])

city_url = ''

keyboard1 = telebot.util.quick_markup({
    'Да ✅': {'callback_data': 'yes'},
    'Нет ❌': {'callback_data': 'no'}
})

keyboard3 = telebot.util.quick_markup({
    'Да ✅': {'callback_data': 'yes_1'},
    'Нет ❌': {'callback_data': 'no_1'}
})

keyboard2 = telebot.util.quick_markup({
    'Сейчас ⚡️': {'callback_data': 'now'},
    'Сегодня 🔍': {'callback_data': 'today'},
    'Завтра ⏱': {'callback_data': 'tomorrow'},
    'Послезавтра ⏰': {'callback_data': '3rd_day'},
    'Другой день 🗓': {'callback_data': 'other_day'}
})


@bot.message_handler(commands=['start', 'restart'])
def start_message(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name}! Я твой помощник по погоде в России!')
        bot.send_message(message.chat.id, 'Погода в каком городе Вас интересует?')
        bot.register_next_step_handler(message, send_message)
    else:
        bot.send_message(message.chat.id, 'Погода в каком городе Вас интересует?')
        bot.register_next_step_handler(message, send_message)


def send_message(message):
    global city_url

    bot.send_message(message.chat.id, '[INFO] Ищу город...')

    introduced_city = message.text.lower()
    possible_city, city_url = parser.find_city(introduced_city)

    if (not possible_city) or (not city_url):
        bot.send_message(message.chat.id, 'Я не нашёл информации по этому городу...\nПожалуйста напишите его корректнее')
        bot.register_next_step_handler(message, send_message)

    bot.send_message(message.chat.id, f'Вам интересна погода в городе {possible_city.title()}:', reply_markup=keyboard2)


def transfer(message):
    bot.send_message(message.chat.id, 'Погода в каком городе Вас интересует?')
    bot.register_next_step_handler(message, send_message)


@bot.callback_query_handler(func=lambda callback: callback.data in ['yes_1', 'no_1'])
def callback_yes_or_no(callback):
    data = callback.data

    if data == 'yes_1':
        transfer(callback.message)
    elif data == 'no_1':
        bot.send_message(callback.message.chat.id, 'Ну ладно буду ждать, пока вы напишете команду /restart')
        bot.send_message(callback.message.chat.id, 'До свидания! 👋')


@bot.callback_query_handler(func=lambda callback: True)
def callback_weather(callback):
    global city_url

    bot.send_message(callback.message.chat.id, '[INFO] Собираю информацию о погоде...')
    if callback.data == 'now':
        data = parser.get_weather_now(city_url)

        if data[0]:
            bot.send_message(callback.message.chat.id, f'🕔 {data[1]}\n🌡 {data[2]}\n🌡 {data[3]}\n💨 {data[4]}\n💧 {data[5]}')
            bot.send_message(callback.message.chat.id, 'Хотите узнать погоду в другом городе?', reply_markup=keyboard3)
        else:
            bot.send_message(callback.message.chat.id, '[INFO] Случилась неожиданная ошибка...')
            bot.send_message(callback.message.chat.id, 'Хотите узнать погоду в другом городе?', reply_markup=keyboard3)

    elif callback.data == 'today':
        data = parser.get_weather_today(city_url)

        if data[0]:
            bot.send_message(callback.message.chat.id, f'🕔 {data[1]}\n🌡 {data[2]}\n🌡 {data[3]}\n💨 {data[4]}\n💧 {data[5]}')
            bot.send_message(callback.message.chat.id, 'Хотите узнать погоду в другом городе?', reply_markup=keyboard3)
        else:
            bot.send_message(callback.message.chat.id, '[INFO] Случилась неожиданная ошибка...')
            bot.send_message(callback.message.chat.id, 'Хотите узнать погоду в другом городе?', reply_markup=keyboard3)


    elif callback.data == 'tomorrow':
        pass

    elif callback.data == '3rd_day':
        pass

    elif callback.data == 'other_day':
        pass


bot.infinity_polling()
